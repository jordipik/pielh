// ============================================================
// PIELH QA Dashboard — app.js
// ============================================================

'use strict';

let data = null;
let map = null;

const layers = {};

// id → L.marker / L.circleMarker for "ver en mapa"
const markerIndex = { buildings: {}, sensors: {} };

// true when real GeoJSON polygons are loaded — suppresses point fallbacks
const geoJsonLoaded = { districts: false, neighborhoods: false };

let filtered = { buildings: [], sensors: [], otherObjects: [] };

// ── QA table state ────────────────────────────────────────────

const state = {
    sort: {
        buildings: { key: 'id', dir: 'asc' },
        sensors: { key: 'id', dir: 'asc' },
    },
    selectedId: null,           // legacy alias — kept for multi-select compat
    selectedThingId: null,      // legacy alias
    selectedBuildingId: null,   // active building context
    selectedSensorId: null,     // active sensor (null = none)
    selectedSensorThingId: null,
    onlyVisibleBld: false,
    onlyVisibleSns: false,
    showLegacySensors: false,
    onlyIotSensorsActive: false,
    onlyIotBuildingsActive: false,
    demoIotMode: false,
    multiSelect: new Set(),
    multiSelectType: null,   // 'building' | 'sensor'
    lastSelectedId: null,
};

let _hlLayer        = null;
let _cityBounds     = null;
let _layersControl  = null;

// ── Helpers ─────────────────────────────────────────────────

async function fetchJson(url, options) {
    const res = await fetch(url, options);
    const text = await res.text();
    let json;
    try {
        json = JSON.parse(text);
    } catch {
        throw new Error(`Respuesta no JSON desde ${url}: ${text.slice(0, 120)}`);
    }
    if (!res.ok) throw new Error(json.error || json.message || `HTTP ${res.status}`);
    return json;
}

function esc(v) {
    if (v == null) return '';
    return String(v)
        .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

function getLat(item) { return item.lat ?? item.Latitud ?? null; }
function getLon(item) { return item.lon ?? item.Longitud ?? null; }
function getName(item) { return item.name ?? item.short_name ?? item.id ?? ''; }
function getDistrict(item) { return item.district_code ?? item.district ?? null; }
function getNeighborhood(item) { return item.neighborhood_key ?? item.neighborhood ?? null; }
function getSystem(item) { return item.system_id ?? null; }
function getBuildingCode(item) { return item.hos ?? item.pielh_id ?? item.id ?? null; }

// ── Key normalization (handles spaces vs underscores, accents, case) ──────────

function normalizeKey(value) {
    if (value == null) return '';
    return String(value)
        .trim()
        .toUpperCase()
        .normalize('NFD')
        .replace(/[̀-ͯ]/g, '')
        .replace(/_/g, ' ')
        .replace(/\s+/g, ' ');
}

function sameKey(a, b) {
    return normalizeKey(a) === normalizeKey(b);
}

function normalizeSystemId(value) {
    const v = normalizeKey(value).replace(/\s/g, '');
    if (v === 'S08') return 'S08A';
    return v;
}

// ── System color palette ─────────────────────────────────────

const SYSTEM_COLORS = {
    S01: '#ef4444', // RUIDO
    S02: '#92400e', // CONTAMINACIÓN EXTERIOR
    S03: '#7c3aed', // GAS RADON
    S04: '#0891b2', // AMBIENTE INTERIOR
    S05: '#ca8a04', // ELECTRICIDAD
    S06: '#2563eb', // AGUA
    S07: '#f97316', // GAS
    S08A: '#b91c1c', // CALDERAS TEMP
    S08B: '#dc2626', // CALDERAS ACS
    S09: '#0ea5e9', // CLIMATIZACIÓN
    S10: '#6b7280', // CONTENEDORES
    S11: '#65a30d', // RIEGO
    S12: '#d97706', // POTENCIA SOLAR
    S13A: '#059669', // SOSTENIBILIDAD EDIFICIOS
    S13B: '#10b981', // ACELERÓMETROS
    S14A: '#0284c7', // METEO
    S14B: '#38bdf8', // SENSOR PIRA
    S15: '#d946ef', // PRESENCIA
    S16: '#8b5cf6', // IPS
    S17: '#ec4899', // AFORO
    S18: '#f43f5e', // TRAFICO
    S19: '#fb923c', // DETECCIÓN FUGAS GAS
    S20: '#3b82f6', // INUNDACION
    S21: '#6366f1', // DETECCIÓN HUMOS
    S22: '#14b8a6', // TRANSPORTE PUBLICO
    S23: '#84cc16', // PARKING
    S24: '#e11d48', // TRAFICO CAM
    S25: '#78716c', // ASCENSORES
    SIP: '#94a3b8', // SENSOR IPS / desconocido
};

function getSystemColor(system_id) {
    return SYSTEM_COLORS[system_id] ?? '#94a3b8';
}

// ── Sensor offset for overlapping points ─────────────────────
// Groups sensors sharing the same coordinate and distributes
// them in a small circle so individual dots remain visible.

const OFFSET_RADIUS = 0.000040; // ~4 m

function offsetOverlappingSensors(sensors) {
    const groups = {};
    sensors.forEach(s => {
        const lat = getLat(s), lon = getLon(s);
        if (lat == null) return;
        const key = `${lat.toFixed(5)},${lon.toFixed(5)}`;
        (groups[key] ??= []).push(s);
    });

    const offsets = {};
    for (const group of Object.values(groups)) {
        if (group.length === 1) {
            const s = group[0];
            offsets[s.id] = { lat: getLat(s), lon: getLon(s) };
            continue;
        }
        const baseLat = getLat(group[0]);
        const baseLon = getLon(group[0]);
        group.forEach((s, i) => {
            const angle = (2 * Math.PI * i) / group.length;
            offsets[s.id] = {
                lat: baseLat + OFFSET_RADIUS * Math.cos(angle),
                lon: baseLon + OFFSET_RADIUS * Math.sin(angle),
            };
        });
    }
    return offsets;
}

// ── GeoJSON boundary loader ──────────────────────────────────
// Loads official polygon boundaries when the GeoJSON files exist.
// Silently falls back to point markers if files are absent (404).

async function loadGeoJsonLayer(url, layerGroup, styleOpts, labelFields) {
    try {
        const res = await fetch(url);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const geojson = await res.json();

        L.geoJSON(geojson, {
            style: styleOpts,
            onEachFeature(feature, leafletLayer) {
                const props = feature.properties ?? {};
                const label = labelFields.map(k => props[k]).find(v => v != null && v !== '')
                    ?? props.NOM ?? props.NOMBRE ?? props.name ?? '—';
                leafletLayer.bindTooltip(String(label), {
                    permanent: false,
                    direction: 'center',
                    className: 'boundary-label',
                });
                leafletLayer.bindPopup(
                    `<div class="popup-title">${esc(String(label))}</div>`,
                    { maxWidth: 260 }
                );
            },
        }).addTo(layerGroup);

        console.info(`GeoJSON cargado: ${url}`);
        return true;
    } catch (e) {
        console.info(`GeoJSON no disponible (${url}): ${e.message} — usando marcadores punto`);
        return false;
    }
}

async function loadBoundaryLayers() {
    geoJsonLoaded.districts = await loadGeoJsonLayer(
        'data/geojson/hospitalet_districtes.geojson',
        layers.districts,
        {
            pane: 'districtsPane',
            color: '#1e40af',
            weight: 3,
            opacity: 0.85,
            fillColor: '#3b82f6',
            fillOpacity: 0.04,
            dashArray: '8 5',
        },
        ['NOM_DIS', 'NOM', 'DISTRICTE', 'NOMBRE_DIS', 'name']
    );

    geoJsonLoaded.neighborhoods = await loadGeoJsonLayer(
        'data/geojson/hospitalet_barris.geojson',
        layers.neighborhoods,
        {
            pane: 'neighborhoodsPane',
            color: '#15803d',
            weight: 2,
            opacity: 0.8,
            fillColor: '#22c55e',
            fillOpacity: 0.06,
        },
        ['NOM_BAR', 'NOM', 'BARRI', 'NOMBRE_BAR', 'name']
    );

    try {
        const res = await fetch('data/geojson/hospitalet_boundary.geojson');
        if (res.ok) {
            const geojson = await res.json();
            const geoLayer = L.geoJSON(geojson, {
                style: { color: '#1e3a5f', weight: 2.5, opacity: 0.85, fill: false, dashArray: '6 4' }
            });
            const b = geoLayer.getBounds();
            if (b.isValid()) _cityBounds = b;
            geoLayer.addTo(layers.cityBoundary);
        }
    } catch {}
}

// ── Load data ────────────────────────────────────────────────

async function loadData() {
    try {
        const res = await fetch('pielh_qa_master.json', { cache: 'no-store' });
        if (!res.ok) throw new Error(`HTTP ${res.status} — ${res.statusText}`);
        data = await res.json();
    } catch (e) {
        document.getElementById('loading-msg').style.display = 'none';
        const err = document.getElementById('error-msg');
        err.textContent = `No se pudo cargar pielh_qa_master.json: ${e.message}. Sirve con Live Server o python -m http.server.`;
        err.style.display = 'block';
        return;
    }

    document.getElementById('loading-msg').style.display = 'none';

    normalizeData();
    initMap();
    await loadBoundaryLayers();   // GeoJSON polygons; fallback to point markers if absent
    requestAnimationFrame(() => { map.invalidateSize(false); zoomToCity(); });
    buildFilters();
    renderSystemsLegend();
    applyFilters();
    renderQA();
    initTables();
    _applyMetaSync(data._meta);
    _checkSyncOnLoad();
    loadPushStatus();
}

// ── Reload data after save (keeps siblings/completed fields in sync) ──

async function reloadData() {
    const res = await fetch('pielh_qa_master.json', { cache: 'no-store' });
    if (!res.ok) throw new Error(`HTTP ${res.status} — ${res.statusText}`);
    data = await res.json();
    normalizeData();
    applyFilters();
    renderQA();
    _applyMetaSync(data._meta);
    loadPushStatus();
}

// ── Normalize / index data ───────────────────────────────────

function normalizeData() {
    data._systemsMap = {};
    (data.catalogs?.systems ?? []).forEach(s => { data._systemsMap[s.id] = s; });

    data._buildingsMap = {};
    data._buildingsByThingId = {};
    (data.buildings ?? []).forEach(b => {
        data._buildingsMap[b.id] = b;
        if (b.thing_id) data._buildingsByThingId[b.thing_id] = b;
    });

    data._sensorsByBuilding = {};
    (data.sensors ?? []).forEach(s => {
        const hos = s.hos ?? getBuildingCode(s);
        if (!hos) return;
        (data._sensorsByBuilding[hos] ??= []).push(s);
    });

    // Split other_objects by type for fast access
    data._otherByType = {};
    (data.other_objects ?? []).forEach(o => {
        (data._otherByType[o.object_type] ??= []).push(o);
    });
}

// ── Map panes ────────────────────────────────────────────────

function initMapPanes() {
    // Lower z-index = drawn first (bottom); higher = drawn on top
    map.createPane('districtsPane').style.zIndex = 200;
    map.createPane('neighborhoodsPane').style.zIndex = 250;
    map.createPane('streetsPane').style.zIndex = 275;
    map.createPane('buildingsPane').style.zIndex = 300;
    map.createPane('sensorsPane').style.zIndex = 420;
    // pointer-events are NOT disabled at pane level; interactive:false
    // on individual background circles handles click pass-through.
}

// ── City zoom ────────────────────────────────────────────────

function zoomToCity() {
    if (_cityBounds?.isValid()) {
        map.fitBounds(_cityBounds, { padding: [30, 30], animate: true });
        return;
    }
    let b = null;
    layers.districts.eachLayer(l => {
        try {
            const lb = l.getBounds?.();
            const ll = l.getLatLng?.();
            if (lb?.isValid()) b = b ? b.extend(lb) : lb;
            else if (ll) b = b ? b.extend(ll) : L.latLngBounds([ll, ll]);
        } catch {}
    });
    if (b?.isValid()) map.fitBounds(b, { padding: [30, 30], animate: true });
    else map.setView([41.365, 2.105], 13, { animate: true });
}

// ── Map init ─────────────────────────────────────────────────

function initMap() {
    map = L.map('map').setView([41.365, 2.105], 13);

    // CartoDB Positron — clean, neutral basemap
    layers.basemap = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '© <a href="https://openstreetmap.org/copyright">OpenStreetMap</a> contributors © <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 19
    }).addTo(map);

    initMapPanes();

    layers.cityBoundary  = L.layerGroup();           // OFF by default; populated async
    layers.districts     = L.layerGroup().addTo(map);
    layers.neighborhoods = L.layerGroup().addTo(map);
    layers.streets       = L.layerGroup();           // OFF by default
    layers.buildings     = L.layerGroup().addTo(map);
    layers.sensors       = L.layerGroup().addTo(map);

    _layersControl = L.control.layers(null, {
        'Límite ciudad': layers.cityBoundary,
        'Mapa de fondo': layers.basemap,
        'Distritos':     layers.districts,
        'Barrios':       layers.neighborhoods,
        'Calles':        layers.streets,
        'Edificios':     layers.buildings,
        'Sensores':      layers.sensors,
    }, { collapsed: false, position: 'topright' }).addTo(map);

    const CityZoom = L.Control.extend({
        onAdd() {
            const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control');
            const btn = L.DomUtil.create('a', '', container);
            btn.href = '#';
            btn.title = 'Ver toda la ciudad';
            btn.innerHTML = '⌂';
            btn.style.fontSize = '16px';
            btn.style.lineHeight = '26px';
            L.DomEvent.disableClickPropagation(btn);
            L.DomEvent.on(btn, 'click', e => {
                L.DomEvent.preventDefault(e);
                zoomToCity();
            });
            return container;
        }
    });
    new CityZoom({ position: 'topleft' }).addTo(map);

    map.on('moveend zoomend', () => {
        if (state.onlyVisibleBld) renderBuildingsList();
        if (state.onlyVisibleSns) renderSensorsList();
    });
}

// ── Filters ──────────────────────────────────────────────────

function buildFilters() {
    populateSelect('filter-district',
        (data.catalogs?.districts ?? []).map(d => ({ value: d.code, label: d.name })));

    populateSelect('filter-neighborhood',
        (data.catalogs?.neighborhoods ?? []).map(n => ({ value: n.key, label: n.name })));

    const catalogSystems = data.catalogs?.systems ?? [];
    const catalogSystemIds = new Set(catalogSystems.map(s => s.id));
    const extraSystems = [];
    [...new Set((data.sensors ?? []).map(s => s.system_id).filter(Boolean))].forEach(id => {
        if (!catalogSystemIds.has(id)) {
            const name = (data.sensors ?? []).find(s => s.system_id === id)?.system_name ?? id;
            extraSystems.push({ id, name });
        }
    });
    populateSelect('filter-system',
        [...catalogSystems, ...extraSystems].map(s => ({ value: s.id, label: `${s.id} — ${s.name}` })));

    const types = [...new Set((data.buildings ?? []).map(b => b.type).filter(Boolean))].sort();
    populateSelect('filter-type', types.map(t => ({ value: t, label: t })));

    const zones = [...new Set((data.buildings ?? []).map(b => b.zone).filter(Boolean))].sort();
    populateSelect('filter-zone', zones.map(z => ({ value: z, label: z })));

    ['filter-district', 'filter-neighborhood', 'filter-system', 'filter-type', 'filter-zone', 'filter-search']
        .forEach(id => {
            const el = document.getElementById(id);
            el.addEventListener('change', applyFilters);
            el.addEventListener('input', applyFilters);
        });
}

function populateSelect(id, options) {
    const sel = document.getElementById(id);
    options.forEach(opt => {
        const el = document.createElement('option');
        el.value = opt.value;
        el.textContent = opt.label;
        sel.appendChild(el);
    });
}

function resetFilters() {
    ['filter-district', 'filter-neighborhood', 'filter-system', 'filter-type', 'filter-zone'].forEach(id => {
        document.getElementById(id).value = '';
    });
    document.getElementById('filter-search').value = '';
    state.onlyIotSensorsActive  = false;
    state.onlyIotBuildingsActive = false;
    state.demoIotMode = false;
    _syncDemoIotCheckboxes();
    _syncDemoIotBtn();
    applyFilters();
}

// ── Apply filters ────────────────────────────────────────────

function applyFilters() {
    const district = document.getElementById('filter-district').value;
    const neighborhood = document.getElementById('filter-neighborhood').value;
    const system = document.getElementById('filter-system').value;
    const type = document.getElementById('filter-type').value;
    const zone = document.getElementById('filter-zone').value;
    const search = document.getElementById('filter-search').value.toLowerCase().trim();

    filtered.buildings = (data.buildings ?? []).filter(b => {
        if (district && b.district_code !== district) return false;
        if (neighborhood && !sameKey(b.neighborhood_key, neighborhood)) return false;
        if (type && b.type !== type) return false;
        if (zone && b.zone !== zone) return false;
        if (system) {
            const bSensors = data._sensorsByBuilding[b.id] ?? [];
            if (!bSensors.some(s => normalizeSystemId(s.system_id) === normalizeSystemId(system))) return false;
        }
        if (search) {
            const hay = [b.id, b.name, b.short_name, b.street_etra, b.neighborhood,
            b.thing_id, b.thing_token, b.state]
                .filter(Boolean).join(' ').toLowerCase();
            if (!hay.includes(search)) return false;
        }
        if (state.onlyIotBuildingsActive) {
            if (!((b.iot_active_sensors ?? 0) > 0 || b.iot_health_status === 'ACTIVE')) return false;
        }
        return true;
    });

    filtered.sensors = (data.sensors ?? []).filter(s => {
        if (!state.showLegacySensors && s.inventory_status === 'LEGACY') return false;
        if (district && s.district_code !== district) return false;
        if (neighborhood && !sameKey(s.neighborhood_key, neighborhood)) return false;
        if (system && normalizeSystemId(s.system_id) !== normalizeSystemId(system)) return false;
        if (type && s.type !== type) return false;
        if (zone && s.zone !== zone) return false;
        if (search) {
            const hay = [s.id, s.hos, s.building_name, s.system_name,
            s.ref_etra, s.thing_id, s.thing_token, s.cu_old, s.neighborhood]
                .filter(Boolean).join(' ').toLowerCase();
            if (!hay.includes(search)) return false;
        }
        if (state.onlyIotSensorsActive) {
            const iot = s.iot_health;
            if (!iot || (!iot.demo_ready && !iot.has_real_data)) return false;
        }
        return true;
    });

    filtered.otherObjects = (data.other_objects ?? []).filter(o => {
        if (!search) return true;
        const hay = [o.id, o.name, o.group, o.object_type, o.thing_id]
            .filter(Boolean).join(' ').toLowerCase();
        return hay.includes(search);
    });

    pruneStaleSelection();

    renderMarkers();
    renderSummary();
    renderIotDemoSummary();
    renderBuildingsList();
    renderSensorsList();
    updateMultiSelectUI();
}

// Quita la selección/tarjeta actual si el registro ya no pertenece al
// resultado filtrado (p.ej. al cambiar de distrito).
function pruneStaleSelection() {
    const visibleIds = new Set([
        ...filtered.buildings.map(b => b.id),
        ...filtered.otherObjects.map(o => o.id),
    ]);

    // Sensors can share the same `id` (legacy duplicates) — a plain id
    // match isn't enough; the specific copy (by thing_id) must be filtered in.
    const isVisible = (id, thingId = null) =>
        visibleIds.has(id) ||
        filtered.sensors.some(s => s.id === id && (!thingId || s.thing_id === thingId));

    if (state.selectedId && !isVisible(state.selectedId, state.selectedThingId)) {
        state.selectedId = null;
        state.selectedThingId = null;
        state.selectedBuildingId = null;
        state.selectedSensorId = null;
        state.selectedSensorThingId = null;
        clearMapHighlight();
    }
    for (const key of [...state.multiSelect]) {
        const found = getRecordByKey(key);
        if (!found || !isVisible(found.record.id, found.record.thing_id || null))
            state.multiSelect.delete(key);
    }
    if (!state.multiSelect.size) state.multiSelectType = null;
}

// ── Render all markers ───────────────────────────────────────

function renderMarkers() {
    layers.buildings.clearLayers();
    layers.sensors.clearLayers();
    layers.streets.clearLayers();
    // GeoJSON boundary layers are static — only clear/re-render when using point fallback
    if (!geoJsonLoaded.neighborhoods) layers.neighborhoods.clearLayers();
    if (!geoJsonLoaded.districts) layers.districts.clearLayers();
    markerIndex.buildings = {};
    markerIndex.sensors = {};

    const sensorOffsets = offsetOverlappingSensors(filtered.sensors);

    filtered.buildings.forEach(b => renderBuildingMarker(b));
    filtered.sensors.forEach(s => renderSensorMarker(s, sensorOffsets));
    if (!geoJsonLoaded.neighborhoods) renderNeighborhoodMarkers();
    if (!geoJsonLoaded.districts) renderDistrictMarkers();
    renderStreetMarkers();
}

// ── Building markers (divIcon square) ────────────────────────

function renderBuildingMarker(b) {
    const lat = getLat(b), lon = getLon(b);
    if (lat == null || lon == null) return;

    const sCount = (data._sensorsByBuilding[b.id] ?? []).length;
    const hasData = (b.has_data ?? '').toUpperCase();

    let statusCls = 'bm-unknown';
    if (b.iot_health_status === 'ACTIVE') statusCls = 'bm-ok';
    else if (b.iot_health_status === 'NO_DATA') statusCls = 'bm-nodata';
    else if (b.iot_health_status === 'NO_SENSORS') statusCls = 'bm-unknown';
    else if (hasData === 'OK') statusCls = 'bm-ok';
    else if (hasData === 'SIN DATOS') statusCls = 'bm-nodata';
    if (b.state === 'Fuera Proyecto') statusCls = 'bm-fuera';

    const labelText = getBuildingCode(b) || b.id || '';
    const icon = L.divIcon({
        className: 'bm-wrap',
        html: `<div class="building-marker ${statusCls}"></div><div class="building-label">${esc(labelText)}</div>`,
        iconSize: [18, 18],
        iconAnchor: [9, 9],
        popupAnchor: [0, -11],
    });

    const marker = L.marker([lat, lon], { icon, pane: 'buildingsPane', zIndexOffset: 0 });
    marker.on('click', () => selectRecord(b.id, { source: 'map', thingId: b.thing_id || null }));
    layers.buildings.addLayer(marker);
    markerIndex.buildings[b.id] = marker;
}

// ── Sensor markers (circleMarker, colored by system) ─────────

function renderSensorMarker(s, offsets) {
    const pos = offsets[s.id];
    if (!pos) return;

    const color = getSystemColor(s.system_id);
    const iot = s.iot_health;
    let fillOpacity = 0.9, weight = 1.5, borderColor = '#fff';
    if (iot) {
        if (iot.demo_ready) { fillOpacity = 0.95; borderColor = '#fff'; }
        else if (iot.has_real_data) { fillOpacity = 0.5; weight = 1; }
        else { fillOpacity = 0.22; weight = 1; }
    }

    const marker = L.circleMarker([pos.lat, pos.lon], {
        pane: 'sensorsPane',
        radius: 6,
        fillColor: color,
        color: borderColor,
        weight: weight,
        fillOpacity: fillOpacity,
    });

    marker.on('click', () => selectRecord(s.id, { source: 'map', thingId: s.thing_id || null }));
    layers.sensors.addLayer(marker);
    markerIndex.sensors[getRecordKey(s)] = marker;
}

// ── Neighborhood markers ──────────────────────────────────────

function renderNeighborhoodMarkers() {
    // Always render all barrios regardless of building/sensor filters;
    // background orientation layers are not subject to data filters.
    const barrios = data._otherByType['OTROS-BARRIOS'] ?? [];

    barrios.forEach(o => {
        const lat = getLat(o), lon = getLon(o);
        if (lat == null || lon == null) return;

        // Large transparent circle — non-interactive (pass clicks through)
        L.circleMarker([lat, lon], {
            pane: 'neighborhoodsPane',
            radius: 32,
            fillColor: '#22c55e',
            color: '#15803d',
            weight: 2,
            fillOpacity: 0.07,
            interactive: false,
        }).addTo(layers.neighborhoods);

        // Clickable label
        const icon = L.divIcon({
            className: '',
            html: `<div class="neighborhood-label">${esc(o.name)}</div>`,
            iconAnchor: [0, 0],
            popupAnchor: [0, -6],
        });
        L.marker([lat, lon], { icon, pane: 'neighborhoodsPane' })
            .bindPopup(otherPopup(o), { maxWidth: 260 })
            .addTo(layers.neighborhoods);
    });
}

// ── District markers ──────────────────────────────────────────

function renderDistrictMarkers() {
    const districts = data._otherByType['OTROS-DISTRITOS'] ?? [];

    districts.forEach(o => {
        const lat = getLat(o), lon = getLon(o);
        if (lat == null || lon == null) return;

        // Dashed boundary circle — non-interactive
        L.circleMarker([lat, lon], {
            pane: 'districtsPane',
            radius: 60,
            fillColor: '#3b82f6',
            color: '#1e40af',
            weight: 3,
            fillOpacity: 0.03,
            dashArray: '8 5',
            interactive: false,
        }).addTo(layers.districts);

        // Short label: "Distrito I", "Distrito II", etc.
        const label = o.name.replace(/ .+$/, '').trim() + ' ' +
            (o.name.match(/[IVX]+/)?.[0] ?? '');
        const icon = L.divIcon({
            className: '',
            html: `<div class="district-label">${esc(label.trim())}</div>`,
            iconAnchor: [0, 0],
            popupAnchor: [0, -8],
        });
        L.marker([lat, lon], { icon, pane: 'districtsPane' })
            .bindPopup(districtPopup(o), { maxWidth: 260 })
            .addTo(layers.districts);
    });
}

// ── Street markers ────────────────────────────────────────────

function renderStreetMarkers() {
    const streets = data._otherByType['OTROS-CALLES'] ?? [];

    streets.forEach(o => {
        const lat = getLat(o), lon = getLon(o);
        if (lat == null || lon == null) return;

        const marker = L.circleMarker([lat, lon], {
            pane: 'streetsPane',
            radius: 5,
            fillColor: '#8b5cf6',
            color: '#6d28d9',
            weight: 1,
            fillOpacity: 0.75,
        });

        // Permanent tooltip with street name
        marker.bindTooltip(esc(o.name), {
            permanent: false,
            direction: 'top',
            offset: [0, -6],
            className: 'street-tooltip',
        });

        marker.bindPopup(otherPopup(o), { maxWidth: 260 });
        layers.streets.addLayer(marker);
    });
}

// ── Popups ───────────────────────────────────────────────────

function row(label, value) {
    if (!value && value !== 0) return '';
    return `<tr><th>${esc(label)}</th><td>${esc(value)}</td></tr>`;
}

function rowMono(label, value) {
    if (!value) return '';
    return `<tr><th>${esc(label)}</th><td class="popup-mono">${esc(value)}</td></tr>`;
}

function buildingPopup(b, sCount) {
    const hasData = b.has_data ?? '—';
    const color = hasData === 'OK' ? '#16a34a' : '#64748b';
    return `
        <div class="popup-title">${esc(b.name)}</div>
        <table class="popup-table">
            ${row('Código HOS', b.id)}
            ${row('Nombre corto', b.short_name)}
            ${row('Dirección', b.street_etra)}
            ${row('Distrito', b.district_name)}
            ${row('Barrio', b.neighborhood)}
            ${row('Tipo', b.type)}
            ${row('Zona', b.zone)}
            ${row('Sensores', sCount)}
            ${row('Estado', b.state)}
            <tr><th>Datos</th><td style="color:${color};font-weight:600">${esc(hasData)}</td></tr>
            ${b.iot_health_status ? row('IoT', `${b.iot_active_sensors ?? 0}/${b.iot_total_sensors ?? 0} activos`) : ''}
            ${rowMono('ThingID', b.thing_id)}
        </table>`;
}

function sensorPopup(s) {
    const color = getSystemColor(s.system_id);
    return `
        <div class="popup-title">
            <span class="popup-sys-dot" style="background:${color}"></span>
            ${esc(s.id)}
        </div>
        <table class="popup-table">
            ${row('Sistema', s.system_name)}
            ${row('Edificio HOS', s.hos)}
            ${row('Edificio', s.building_name)}
            ${row('Barrio', s.neighborhood)}
            ${row('Distrito', s.district_name)}
            ${row('Tipo', s.type)}
            ${row('REF-ETRA', s.ref_etra)}
            ${row('Datos', s.has_data)}
            ${s.iot_health ? row('IoT estado', s.iot_health.status) : ''}
            ${s.iot_health?.resource ? row('IoT recurso', s.iot_health.resource) : ''}
            ${s.iot_health?.last_seen ? row('Ultima lectura', s.iot_health.last_seen.slice(0, 16).replace('T', ' ')) : ''}
            ${rowMono('ThingID', s.thing_id)}
            ${rowMono('ThingToken', s.thing_token)}
        </table>`;
}

function otherPopup(o) {
    return `
        <div class="popup-title">${esc(o.name)}</div>
        <table class="popup-table">
            ${row('Tipo', o.object_type)}
            ${row('Grupo', o.group)}
            ${row('Datos', o.has_data)}
            ${rowMono('ThingID', o.thing_id)}
            ${rowMono('ThingToken', o.thing_token)}
        </table>`;
}

function districtPopup(o) {
    // Match with catalog to show stats
    const cat = (data.catalogs?.districts ?? []).find(d =>
        o.name.includes(d.name) || d.description === o.name
    );
    return `
        <div class="popup-title">${esc(o.name)}</div>
        <table class="popup-table">
            ${cat ? row('Edificios', cat.building_count) : ''}
            ${cat ? row('Sensores', cat.sensor_count) : ''}
            ${rowMono('ThingID', o.thing_id)}
        </table>`;
}

// ── IoT Demo Summary ─────────────────────────────────────────

function renderIotDemoSummary() {
    const el = document.getElementById('iot-demo-summary');
    if (!el) return;

    const allSensors   = data.sensors   ?? [];
    const allBuildings = data.buildings ?? [];

    const activeSensors   = allSensors.filter(s => s.iot_health?.demo_ready || s.iot_health?.has_real_data);
    const activeBuildings = allBuildings.filter(b => (b.iot_active_sensors ?? 0) > 0);
    const activeSysIds    = new Set(activeSensors.map(s => s.system_id).filter(Boolean));

    const total = allSensors.length;
    const pct   = total > 0 ? (activeSensors.length / total * 100).toFixed(1) : '0.0';

    el.innerHTML =
        `<div class="iot-summary-row"><span class="iot-summary-val">${activeSensors.length}</span><span class="iot-summary-lbl"> sensores IoT activos</span></div>` +
        `<div class="iot-summary-row"><span class="iot-summary-val">${activeBuildings.length}</span><span class="iot-summary-lbl"> edificios con IoT activo</span></div>` +
        `<div class="iot-summary-row"><span class="iot-summary-val">${activeSysIds.size}</span><span class="iot-summary-lbl"> sistemas IoT activos</span></div>` +
        `<div class="iot-summary-row"><span class="iot-summary-val">${pct}%</span><span class="iot-summary-lbl"> cobertura de datos</span></div>`;
}

// ── Summary cards ────────────────────────────────────────────

function renderSummary() {
    document.getElementById('count-buildings').textContent = filtered.buildings.length;
    document.getElementById('count-sensors').textContent = filtered.sensors.length;
    const legacyEl = document.getElementById('count-sensors-legacy');
    if (legacyEl) {
        const nLegacy = (data.sensors ?? []).filter(s => s.inventory_status === 'LEGACY').length;
        legacyEl.textContent = nLegacy
            ? (state.showLegacySensors ? `incl. ${nLegacy} LEGACY` : `+${nLegacy} ocultos`)
            : '';
    }
    document.getElementById('count-neighborhoods').textContent = (data.catalogs?.neighborhoods ?? []).length;
    document.getElementById('count-systems').textContent = (data.catalogs?.systems ?? []).length;
    document.getElementById('count-qa').textContent = (data.qa?.findings ?? []).length;
}

// ── Buildings list ───────────────────────────────────────────

function renderBuildingsList() {
    let records = filtered.buildings;
    if (state.onlyVisibleBld) records = getMapVisible(records);
    records = sortRecords(records, state.sort.buildings);
    _lastBuildingRecords = records;

    const total = (data.buildings ?? []).length;
    const filt = filtered.buildings.length;
    document.getElementById('buildings-info').textContent = state.onlyVisibleBld
        ? `${records.length} visibles · ${filt} filtrados de ${total}`
        : `${filt} de ${total} edificios`;

    updateSortIcons('list-thead', state.sort.buildings);

    const tbody = document.getElementById('list-tbody');
    tbody.innerHTML = '';
    records.forEach(b => {
        const sCount = (data._sensorsByBuilding[b.id] ?? []).length;
        const hasData = (b.has_data ?? '').toUpperCase();
        const dataColor = hasData === 'OK' ? '#16a34a' : '#94a3b8';
        const tr = document.createElement('tr');
        tr.dataset.rid = b.id;
        tr.dataset.key = getRecordKey(b);
        if (b.id === state.selectedBuildingId) tr.classList.add('row-selected');
        if (b.state === 'Fuera Proyecto') tr.classList.add('row-fuera');
        tr.innerHTML = `
            <td title="${esc(b.id)}">${esc(b.id)}</td>
            <td title="${esc(b.name)}">${esc(truncate(b.name || b.short_name, 30))}</td>
            <td title="${esc(b.type)}">${esc(b.type ?? '—')}</td>
            <td title="${esc(b.neighborhood)}">${esc(shortNeighborhood(b.neighborhood))}</td>
            <td title="${esc(b.district_name)}">${esc(b.district_name ?? '—')}</td>
            <td title="${esc(b.street_etra)}">${esc(truncate(b.street_etra, 20))}</td>
            <td>${sCount}</td>
            <td>${b.iot_health_status
                ? `<span class="iot-badge iot-${b.iot_health_status.toLowerCase()}">${b.iot_active_sensors ?? 0}/${b.iot_total_sensors ?? 0}</span>`
                : `<span style="color:${dataColor};font-weight:600">${esc(b.has_data ?? '—')}</span>`}</td>
            <td title="${esc(b.thing_id ?? '')}">${b.thing_id ? esc(truncate(b.thing_id, 16)) : '—'}</td>
        `;
        tr.addEventListener('click', e => {
            if (e.ctrlKey || e.metaKey) {
                toggleMultiSelect(getRecordKey(b), 'building');
            } else if (e.shiftKey && state.lastSelectedId) {
                rangeMultiSelect(getRecordKey(b), 'building', _lastBuildingRecords);
            } else {
                clearMultiSelect();
                selectRecord(b.id, { source: 'table', thingId: b.thing_id || null });
            }
        });
        tbody.appendChild(tr);
    });
}

// ── Sensors list ─────────────────────────────────────────────

const SENSOR_LIMIT = 500;

function renderSensorsList() {
    let records = filtered.sensors;
    const selBldId = state.selectedBuildingId || null;
    if (selBldId) records = records.filter(s => s.hos === selBldId);
    _lastSensorRecords = records;
    if (state.onlyVisibleSns) records = getMapVisible(records);
    records = sortRecords(records, state.sort.sensors);
    const limited = records.length > SENSOR_LIMIT;
    if (limited) records = records.slice(0, SENSOR_LIMIT);

    const total = (data.sensors ?? []).length;
    const filt = filtered.sensors.length;
    const bldSuffix = selBldId ? ` · edificio ${selBldId}` : '';
    document.getElementById('sensors-info').textContent = state.onlyVisibleSns
        ? `${records.length} visibles · ${filt} filtrados de ${total}${limited ? ' (límite 500)' : ''}${bldSuffix}`
        : `${selBldId ? records.length : filt} de ${total} sensores${limited ? ' (mostrando 500)' : ''}${bldSuffix}`;

    updateSortIcons('sensors-thead', state.sort.sensors);

    const tbody = document.getElementById('sensors-tbody');
    tbody.innerHTML = '';
    records.forEach(s => {
        const color = getSystemColor(s.system_id);
        const hasData = (s.has_data ?? '').toUpperCase();
        const dataColor = hasData === 'OK' ? '#16a34a' : '#94a3b8';
        const isLegacy = s.inventory_status === 'LEGACY';
        const tr = document.createElement('tr');
        tr.dataset.rid = s.id;
        tr.dataset.key = getRecordKey(s);
        tr.dataset.thingId = s.thing_id || '';
        if (isLegacy) tr.classList.add('row-legacy');
        if (s.id === state.selectedSensorId && (!state.selectedSensorThingId || s.thing_id === state.selectedSensorThingId))
            tr.classList.add('row-selected');
        tr.innerHTML = `
            <td title="${esc(s.id)}">${esc(truncate(s.id, 18))}${isLegacy ? ' <span class="badge badge-legacy">LEGACY</span>' : ''}</td>
            <td>${esc(s.hos ?? '—')}</td>
            <td title="${esc(s.system_name)}">
                <span class="sys-dot" style="background:${color}"></span>${esc(s.system_id ?? '—')}
            </td>
            <td title="${esc(s.neighborhood)}">${esc(shortNeighborhood(s.neighborhood))}</td>
            <td title="${esc(s.district_name)}">${esc(s.district_name ?? '—')}</td>
            <td title="${esc(s.ref_etra)}">${esc(truncate(s.ref_etra, 18))}</td>
            <td>${s.iot_health
                ? `<span class="iot-badge iot-${s.iot_health.demo_ready ? 'active' : 'nodata'}">${esc(s.iot_health.status)}</span>`
                : `<span style="color:${dataColor};font-weight:600">${esc(s.has_data ?? '—')}</span>`}</td>
            <td title="${esc(s.thing_id ?? '')}">${s.thing_id ? esc(truncate(s.thing_id, 16)) : '—'}</td>
        `;
        tr.addEventListener('click', e => {
            if (e.ctrlKey || e.metaKey) {
                toggleMultiSelect(getRecordKey(s), 'sensor');
            } else if (e.shiftKey && state.lastSelectedId) {
                rangeMultiSelect(getRecordKey(s), 'sensor', _lastSensorRecords);
            } else {
                clearMultiSelect();
                selectRecord(s.id, { source: 'table', thingId: s.thing_id });
            }
        });
        tbody.appendChild(tr);
    });
}

// ── Focus on map ─────────────────────────────────────────────

function focusBuilding(id) {
    const b = data._buildingsMap[id];
    if (!b) return;
    const lat = getLat(b), lon = getLon(b);
    if (lat == null) return;

    if (!map.hasLayer(layers.buildings)) map.addLayer(layers.buildings);
    map.setView([lat, lon], 17, { animate: true });
}

function focusSensor(id, thingId = null) {
    const s = findSensor(id, thingId);
    if (!s) return;
    const lat = getLat(s), lon = getLon(s);
    if (lat == null) return;

    if (!map.hasLayer(layers.sensors)) map.addLayer(layers.sensors);
    map.setView([lat, lon], 17, { animate: true });
}

// Returns the operational key for a record: thing_id when available, id otherwise.
function getRecordKey(record) {
    return record.thing_id || record.id;
}

// Resolves a record from a key (thing_id or id). Returns { record, type } or null.
function getRecordByKey(key) {
    const b = data._buildingsMap[key] || data._buildingsByThingId?.[key];
    if (b) return { record: b, type: 'building' };
    const s = (data.sensors ?? []).find(s => s.thing_id === key) ||
              (data.sensors ?? []).find(s => s.id === key);
    if (s) return { record: s, type: 'sensor' };
    return null;
}

// Sensors may share the same `id` (legacy duplicates) — when a specific
// thing_id is known, prefer the matching copy; otherwise fall back to the
// first occurrence.
function findSensor(id, thingId = null) {
    const matches = (data.sensors ?? []).filter(s => s.id === id);
    if (thingId) {
        const m = matches.find(s => s.thing_id === thingId);
        if (m) return m;
    }
    return matches[0];
}

// ── Map highlight ─────────────────────────────────────────────

function clearMapHighlight() {
    if (_hlLayer) { map.removeLayer(_hlLayer); _hlLayer = null; }
}

function highlightMapRecord(id, type, thingId = null) {
    clearMapHighlight();
    const sKey = type === 'sensor' ? (thingId || id) : id;
    const m = type === 'building' ? markerIndex.buildings[id] : markerIndex.sensors[sKey];
    if (!m) return;
    _hlLayer = L.circleMarker(m.getLatLng(), {
        pane: 'sensorsPane',
        radius: type === 'building' ? 18 : 14,
        color: '#f59e0b',
        weight: 3,
        fillColor: '#fde68a',
        fillOpacity: 0.45,
        interactive: false,
    }).addTo(map);
}

// ── Central record selection ──────────────────────────────────

function selectRecord(id, opts = {}) {
    const { source = 'table', thingId = null } = opts;

    document.querySelectorAll('tr.row-selected').forEach(r => r.classList.remove('row-selected'));
    clearMapHighlight();
    if (!id) return;

    const isBuilding = !!data._buildingsMap[id];

    if (isBuilding) {
        // Building selected: set building context, clear sensor
        state.selectedBuildingId    = id;
        state.selectedSensorId      = null;
        state.selectedSensorThingId = null;
        state.selectedId            = id;
        state.selectedThingId       = thingId || data._buildingsMap[id]?.thing_id || null;

        highlightMapRecord(id, 'building');
        if (source === 'map') {
            const btn = document.querySelector('[data-tab="tab-buildings"]');
            if (btn && !document.getElementById('tab-buildings').classList.contains('active'))
                showTab(btn, 'tab-buildings');
        }
    } else {
        // Sensor selected: activate sensor + auto-set building context from hos
        const s = findSensor(id, thingId);
        if (s) {
            state.selectedSensorId      = id;
            state.selectedSensorThingId = thingId;
            state.selectedId            = id;
            state.selectedThingId       = thingId;
            // Auto-select parent building if sensor has hos
            if (s.hos && data._buildingsMap[s.hos]) {
                state.selectedBuildingId = s.hos;
            }
            highlightMapRecord(id, 'sensor', thingId);
            if (source === 'map') {
                const btn = document.querySelector('[data-tab="tab-sensors"]');
                if (btn && !document.getElementById('tab-sensors').classList.contains('active'))
                    showTab(btn, 'tab-sensors');
            }
        }
    }

    // Highlight rows
    const bldRow = document.querySelector(`tr[data-rid="${CSS.escape(state.selectedBuildingId || '')}"]`);
    if (bldRow) { bldRow.classList.add('row-selected'); bldRow.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); }
    const sensKey = !isBuilding ? (thingId || id) : null;
    const sensRow = sensKey ? document.querySelector(`tr[data-key="${CSS.escape(sensKey)}"]`) : null;
    if (sensRow) { sensRow.classList.add('row-selected'); sensRow.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); }

    renderSelectionBar();
    renderSensorsList();
}

// ── Visible-in-map filter ─────────────────────────────────────

function getMapVisible(records) {
    const bounds = map.getBounds();
    return records.filter(r => {
        const lat = getLat(r), lon = getLon(r);
        return lat != null && bounds.contains([lat, lon]);
    });
}

// ── Sort ──────────────────────────────────────────────────────

function sortRecords(records, sortState) {
    const { key, dir } = sortState;
    const mult = dir === 'asc' ? 1 : -1;
    return [...records].sort((a, b) => {
        let va = key === '_sCount' ? (data._sensorsByBuilding[a.id] ?? []).length : a[key];
        let vb = key === '_sCount' ? (data._sensorsByBuilding[b.id] ?? []).length : b[key];
        if (va == null) va = ''; if (vb == null) vb = '';
        if (typeof va === 'number' && typeof vb === 'number') return mult * (va - vb);
        return mult * String(va).localeCompare(String(vb), 'ca', { sensitivity: 'base' });
    });
}

function updateSortIcons(theadId, sortState) {
    document.querySelectorAll(`#${theadId} th[data-sort]`).forEach(th => {
        const icon = th.querySelector('.sort-icon');
        if (!icon) return;
        const active = th.dataset.sort === sortState.key;
        icon.textContent = active ? (sortState.dir === 'asc' ? '▲' : '▼') : '';
        th.classList.toggle('sort-active', active);
    });
}

// ── Panel resizer ─────────────────────────────────────────────

function initPanelResizer() {
    const panel = document.querySelector('.right-panel');
    const handle = document.getElementById('panel-resizer');
    if (!panel || !handle) return;

    const saved = localStorage.getItem('pielh_panelW');
    if (saved) panel.style.flexBasis = saved + 'px';

    handle.addEventListener('mousedown', e => {
        e.preventDefault();
        const startX = e.clientX, startW = panel.offsetWidth;
        const onMove = e => {
            const w = Math.min(Math.max(startW - (e.clientX - startX), 280), 900);
            panel.style.flexBasis = w + 'px';
        };
        const onUp = () => {
            localStorage.setItem('pielh_panelW', panel.offsetWidth);
            document.body.style.cursor = document.body.style.userSelect = '';
            document.removeEventListener('mousemove', onMove);
            document.removeEventListener('mouseup', onUp);
        };
        document.body.style.cursor = 'col-resize';
        document.body.style.userSelect = 'none';
        document.addEventListener('mousemove', onMove);
        document.addEventListener('mouseup', onUp);
    });
}

// ── Resizable columns ─────────────────────────────────────────

function initResizableColumns(tableId) {
    const table = document.getElementById(tableId);
    if (!table) return;
    const saved = JSON.parse(localStorage.getItem('pielh_colW_' + tableId) || '{}');

    table.querySelectorAll('thead th').forEach((th, i) => {
        if (saved[i]) th.style.minWidth = saved[i] + 'px';
        const handle = document.createElement('span');
        handle.className = 'col-resizer';
        th.appendChild(handle);
        handle.addEventListener('mousedown', e => {
            e.preventDefault(); e.stopPropagation();
            const startX = e.clientX, startW = th.offsetWidth;
            const onMove = e => { th.style.minWidth = Math.max(startW + (e.clientX - startX), 36) + 'px'; };
            const onUp = () => {
                const widths = {};
                table.querySelectorAll('thead th').forEach((t, j) => { widths[j] = t.offsetWidth; });
                localStorage.setItem('pielh_colW_' + tableId, JSON.stringify(widths));
                document.body.style.cursor = document.body.style.userSelect = '';
                document.removeEventListener('mousemove', onMove);
                document.removeEventListener('mouseup', onUp);
            };
            document.body.style.cursor = 'col-resize';
            document.body.style.userSelect = 'none';
            document.addEventListener('mousemove', onMove);
            document.addEventListener('mouseup', onUp);
        });
    });
}

// ── Table sort + visible wiring ───────────────────────────────

function initTables() {
    // Sort click on buildings headers
    document.querySelectorAll('#list-thead th[data-sort]').forEach(th => {
        th.addEventListener('click', e => {
            if (e.target.classList.contains('col-resizer')) return;
            const key = th.dataset.sort;
            const s = state.sort.buildings;
            s.dir = (s.key === key && s.dir === 'asc') ? 'desc' : 'asc';
            s.key = key;
            renderBuildingsList();
        });
    });

    // Sort click on sensors headers
    document.querySelectorAll('#sensors-thead th[data-sort]').forEach(th => {
        th.addEventListener('click', e => {
            if (e.target.classList.contains('col-resizer')) return;
            const key = th.dataset.sort;
            const s = state.sort.sensors;
            s.dir = (s.key === key && s.dir === 'asc') ? 'desc' : 'asc';
            s.key = key;
            renderSensorsList();
        });
    });

    // Visible-only checkboxes
    document.getElementById('chk-visible-bld').addEventListener('change', e => {
        state.onlyVisibleBld = e.target.checked;
        renderBuildingsList();
    });
    document.getElementById('chk-show-legacy').addEventListener('change', e => {
        state.showLegacySensors = e.target.checked;
        applyFilters();
    });
    document.getElementById('chk-visible-sns').addEventListener('change', e => {
        state.onlyVisibleSns = e.target.checked;
        renderSensorsList();
    });

    // IoT demo controls
    document.getElementById('chk-iot-sensors-active').addEventListener('change', e => {
        state.onlyIotSensorsActive = e.target.checked;
        if (!e.target.checked) state.demoIotMode = false;
        _syncDemoIotBtn();
        applyFilters();
    });
    document.getElementById('chk-iot-buildings-active').addEventListener('change', e => {
        state.onlyIotBuildingsActive = e.target.checked;
        if (!e.target.checked) state.demoIotMode = false;
        _syncDemoIotBtn();
        applyFilters();
    });
    document.getElementById('btn-demo-iot').addEventListener('click', () => {
        state.demoIotMode = !state.demoIotMode;
        state.onlyIotSensorsActive  = state.demoIotMode;
        state.onlyIotBuildingsActive = state.demoIotMode;
        _syncDemoIotCheckboxes();
        _syncDemoIotBtn();
        applyFilters();
    });

    initResizableColumns('buildings-table');
    initResizableColumns('sensors-table');
    initPanelResizer();
}

function _syncDemoIotCheckboxes() {
    document.getElementById('chk-iot-sensors-active').checked  = state.onlyIotSensorsActive;
    document.getElementById('chk-iot-buildings-active').checked = state.onlyIotBuildingsActive;
}
function _syncDemoIotBtn() {
    document.getElementById('btn-demo-iot')
        .classList.toggle('btn-demo-iot-active', state.demoIotMode);
}

// ── QA Panel ─────────────────────────────────────────────────

function renderQA() {
    const findings = data.qa?.findings ?? [];

    const bySeverity = {};
    const byType = {};
    findings.forEach(f => {
        bySeverity[f.severity] = (bySeverity[f.severity] ?? 0) + 1;
        byType[f.type] = (byType[f.type] ?? 0) + 1;
    });

    document.getElementById('qa-severity-badges').innerHTML = Object.entries(bySeverity)
        .map(([sev, cnt]) =>
            `<span class="badge badge-${sev.toLowerCase()}">${esc(sev)}: ${cnt}</span>`)
        .join('');

    const sevSel = document.getElementById('qa-filter-severity');
    sevSel.innerHTML = '<option value="">Todas las severidades</option>';
    Object.keys(bySeverity).sort().forEach(sev => {
        const opt = document.createElement('option');
        opt.value = sev; opt.textContent = `${sev} (${bySeverity[sev]})`;
        sevSel.appendChild(opt);
    });

    const typeSel = document.getElementById('qa-filter-type');
    typeSel.innerHTML = '<option value="">Todos los tipos</option>';
    Object.entries(byType).sort().forEach(([type, cnt]) => {
        const opt = document.createElement('option');
        opt.value = type; opt.textContent = `${type} (${cnt})`;
        typeSel.appendChild(opt);
    });

    renderQARows(findings);
}

function renderQARows(findings) {
    const tbody = document.getElementById('qa-tbody');
    tbody.innerHTML = '';
    findings.forEach(f => {
        const details = Object.entries(f)
            .filter(([k]) => k !== 'severity' && k !== 'type')
            .map(([k, v]) => `<span style="color:#64748b">${esc(k)}:</span> ${esc(v)}`)
            .join('<br>');
        const tr = document.createElement('tr');
        tr.dataset.severity = f.severity;
        tr.dataset.type = f.type;
        tr.innerHTML = `
            <td><span class="badge badge-${(f.severity ?? 'info').toLowerCase()}">${esc(f.severity)}</span></td>
            <td class="qa-type-label" title="${esc(f.type)}">${esc(f.type)}</td>
            <td class="qa-type-label">${details}</td>
        `;
        tbody.appendChild(tr);
    });
}

function filterQA() {
    const sev = document.getElementById('qa-filter-severity').value;
    const type = document.getElementById('qa-filter-type').value;
    document.querySelectorAll('#qa-tbody tr').forEach(tr => {
        const sevMatch = !sev || tr.dataset.severity === sev;
        const typeMatch = !type || tr.dataset.type === type;
        tr.style.display = sevMatch && typeMatch ? '' : 'none';
    });
}

// ── Systems legend ────────────────────────────────────────────

const LEGEND_SYSTEMS = [
    ['S01', 'RUIDO'], ['S02', 'CONTAM. EXT.'], ['S03', 'GAS RADÓN'],
    ['S04', 'AMBIENTE'], ['S05', 'ELECTRIC.'], ['S06', 'AGUA'],
    ['S07', 'GAS'], ['S08A', 'CALDERAS'], ['S09', 'CLIMAT.'],
    ['S13A', 'SOSTENIB.'], ['S14A', 'METEO'], ['S15', 'PRESENCIA'],
    ['S19', 'FUGAS GAS'], ['S20', 'INUNDACIÓN'], ['S21', 'HUMOS'],
    ['S22', 'TRANS. PÚB.'],
];

function renderSystemsLegend() {
    const el = document.getElementById('legend-systems');
    if (!el) return;
    el.innerHTML = LEGEND_SYSTEMS.map(([id, label]) => `
        <div class="legend-row">
            <span class="ldot" style="background:${getSystemColor(id)};border-color:${getSystemColor(id)};opacity:0.9"></span>
            <span class="legend-sys-id">${id}</span>
            <span class="legend-sys-name">${label}</span>
        </div>
    `).join('');
}

// ── Tab switching ─────────────────────────────────────────────

function showTab(btn, tabId) {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(tabId).classList.add('active');
    if (tabId === 'tab-sync') initSyncTab();
}

// ============================================================
// CENTRO DE SINCRONIZACIÓN IoT
// ============================================================

let _systemSyncPollTimer = null;
let _systemSyncData      = [];
let _syncSelectedSet     = new Set();

async function initSyncTab() {
    if (_systemSyncData.length === 0) await refreshSyncCenter();
}

async function refreshSyncCenter() {
    try {
        const r = await fetchJson('/api/systems-status');
        _systemSyncData = r.systems || [];
        renderSyncTable(_systemSyncData);
    } catch (e) {
        showToast('Error al cargar sistemas: ' + e.message, false);
    }
}

function renderSyncTable(systems) {
    const tbody = document.getElementById('sync-tbody');
    if (!tbody) return;
    const filter = (document.querySelector('input[name="sync-filter"]:checked') || {}).value || 'all';
    let rows = systems;
    if (filter === 'active')  rows = systems.filter(s => s.status === 'ACTIVE');
    if (filter === 'no_data') rows = systems.filter(s => s.status === 'NO_DATA');
    if (filter === 'partial') rows = systems.filter(s => s.status === 'PARTIAL');
    if (filter === 'error')   rows = systems.filter(s => s.status === 'ERROR');

    const totalCount    = systems.reduce((a, s) => a + s.count, 0);
    const totalWith     = systems.reduce((a, s) => a + s.with_data, 0);
    const totalWithout  = systems.reduce((a, s) => a + s.without_data, 0);

    let html = `<tr class="sync-row-all">
        <td><input type="checkbox" class="sync-chk" value="ALL" onchange="toggleSyncCheck(this)"></td>
        <td colspan="2"><strong>TODOS</strong></td>
        <td>${totalCount}</td>
        <td>${totalWith}</td>
        <td>${totalWithout}</td>
        <td>—</td><td>—</td><td>—</td>
        <td><button class="btn-sync-system" onclick="syncSystem('ALL')">Sincronizar todos</button></td>
    </tr>`;

    for (const sys of rows) {
        const checked  = _syncSelectedSet.has(sys.system_id) ? 'checked' : '';
        const badge    = _syncStatusBadge(sys.status);
        const lastSeen = _relativeTime(sys.last_seen);
        const lss      = sys.last_sync;
        const lastSync = lss
            ? `${_fmtDT(lss.at)} ${lss.ok ? '<span class="sync-ok">OK</span>' : '<span class="sync-err">ERR</span>'}`
            : '—';
        html += `<tr data-status="${sys.status || ''}">
            <td><input type="checkbox" class="sync-chk" value="${sys.system_id}" ${checked} onchange="toggleSyncCheck(this)"></td>
            <td>${sys.system_id}</td>
            <td title="${sys.label || ''}">${sys.system_name}</td>
            <td>${sys.count}</td>
            <td>${sys.with_data}</td>
            <td>${sys.without_data}</td>
            <td>${lastSeen}</td>
            <td>${badge}</td>
            <td class="sync-last-sync">${lastSync}</td>
            <td><button class="btn-sync-system" onclick="syncSystem('${sys.system_id}')">Sincronizar</button></td>
        </tr>`;
    }
    tbody.innerHTML = html;
    _updateSyncSelectedBtn();
}

function _syncStatusBadge(status) {
    const cls = { ACTIVE: 'active', PARTIAL: 'partial', NO_DATA: 'nodata', ERROR: 'error' };
    const c = cls[status] || '';
    return `<span class="sync-badge${c ? ' sync-badge-' + c : ''}">${status || '?'}</span>`;
}

function filterSyncTable() {
    renderSyncTable(_systemSyncData);
}

function toggleSyncCheck(cb) {
    const val = cb.value;
    if (val === 'ALL') {
        _syncSelectedSet.clear();
        if (cb.checked) _systemSyncData.forEach(s => _syncSelectedSet.add(s.system_id));
        document.querySelectorAll('.sync-chk:not([value="ALL"])').forEach(c => { c.checked = cb.checked; });
    } else {
        if (cb.checked) _syncSelectedSet.add(val);
        else _syncSelectedSet.delete(val);
    }
    _updateSyncSelectedBtn();
}

function toggleAllSyncCheck(cb) {
    _syncSelectedSet.clear();
    if (cb.checked) _systemSyncData.forEach(s => _syncSelectedSet.add(s.system_id));
    document.querySelectorAll('.sync-chk').forEach(c => { c.checked = cb.checked; });
    _updateSyncSelectedBtn();
}

function _updateSyncSelectedBtn() {
    const btn = document.getElementById('btn-sync-selected');
    if (!btn) return;
    const n = _syncSelectedSet.size;
    btn.disabled = n === 0;
    btn.textContent = n > 0 ? `↓ Sincronizar seleccionados (${n})` : '↓ Sincronizar seleccionados';
}

async function syncSystem(systemId) {
    if (systemId === 'ALL') return syncSelected(_systemSyncData.map(s => s.system_id));
    return syncSelected([systemId]);
}

async function syncSelected(overrideList) {
    const systems = overrideList || [..._syncSelectedSet];
    if (!systems.length) return;
    _showSyncProgress(systems);
    try {
        let endpoint, body;
        if (systems.length === 1) {
            endpoint = '/api/import-system';
            body = JSON.stringify({ system_id: systems[0] });
        } else {
            endpoint = '/api/import-selected';
            body = JSON.stringify({ systems });
        }
        await fetchJson(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body });
        _pollSystemSync(systems);
    } catch (e) {
        showToast('Error al iniciar sincronización: ' + e.message, false);
        const area = document.getElementById('sync-progress-area');
        if (area) area.style.display = 'none';
    }
}

function _showSyncProgress(systems) {
    const area = document.getElementById('sync-progress-area');
    if (!area) return;
    area.style.display = 'block';
    area.innerHTML = systems.map((sid, i) =>
        `<div class="sync-prog-row">
            <span class="sync-prog-label">[${i + 1}/${systems.length}] ${sid}</span>
            <div class="sync-prog-bar-wrap"><div class="sync-prog-bar" id="sync-bar-${sid}" style="width:0%"></div></div>
            <span class="sync-prog-status" id="sync-stat-${sid}">Pendiente</span>
        </div>`
    ).join('');
}

function _pollSystemSync(systems) {
    clearTimeout(_systemSyncPollTimer);
    _systemSyncPollTimer = setTimeout(async () => {
        try {
            const s = await fetchJson('/api/system-sync-status');
            _updateSystemSyncUI(s, systems);
            if (s.running) {
                _pollSystemSync(systems);
            } else {
                if (s.done && !s.error) {
                    systems.forEach(sid => {
                        const bar  = document.getElementById(`sync-bar-${sid}`);
                        const stat = document.getElementById(`sync-stat-${sid}`);
                        if (bar)  { bar.style.width = '100%'; bar.style.background = '#4ade80'; }
                        if (stat) stat.textContent = 'OK';
                    });
                    await reloadData();
                    await refreshSyncCenter();
                    showToast(`Sincronización completada: ${systems.join(', ')}`, true);
                } else if (s.error) {
                    showToast('Error en sincronización: ' + s.error, false);
                }
                setTimeout(() => {
                    const area = document.getElementById('sync-progress-area');
                    if (area) area.style.display = 'none';
                }, 3000);
            }
        } catch (_) { _pollSystemSync(systems); }
    }, 1200);
}

function _updateSystemSyncUI(s, systems) {
    const idx = s.current_idx || 0;
    systems.forEach((sid, i) => {
        const bar  = document.getElementById(`sync-bar-${sid}`);
        const stat = document.getElementById(`sync-stat-${sid}`);
        if (!bar || !stat) return;
        if (i < idx) {
            bar.style.width = '100%'; bar.style.background = '#4ade80';
            stat.textContent = 'OK';
        } else if (i === idx && s.running) {
            const pct = Math.min(85, 10 + (s.things_done || 0) * 2);
            bar.style.width = pct + '%'; bar.style.background = '#3b82f6';
            stat.textContent = `${s.things_done || 0} things…`;
        }
    });
}

async function analyzeSystems() {
    showToast('Actualizando estado IoT de sistemas…', true);
    await refreshSyncCenter();
}

function _relativeTime(isoStr) {
    if (!isoStr) return '—';
    const diff = Date.now() - new Date(isoStr).getTime();
    const m    = Math.floor(diff / 60000);
    if (m < 1)   return 'ahora';
    if (m < 60)  return `hace ${m} min`;
    const h = Math.floor(m / 60);
    if (h < 24)  return `hace ${h}h`;
    return `hace ${Math.floor(h / 24)}d`;
}

function _fmtDT(isoStr) {
    if (!isoStr) return '—';
    return new Date(isoStr).toLocaleString('es-ES', {
        day: '2-digit', month: '2-digit', year: 'numeric',
        hour: '2-digit', minute: '2-digit',
    });
}

// ── Utilities ────────────────────────────────────────────────

function truncate(str, max) {
    if (!str) return '';
    return str.length > max ? str.slice(0, max) + '…' : str;
}

function shortNeighborhood(n) {
    if (!n) return '—';
    return n.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

// ── Bootstrap ────────────────────────────────────────────────

loadData();

// ============================================================
// EDIT PANEL
// ============================================================

// Module-level vars

let _lastBuildingRecords = [];
let _lastSensorRecords = [];
let _pendingCopyChanges = null;

const editState = {
    entityType: null,   // 'sensor' | 'building'
    ids: [],            // compat: deduplicated ids (may omit siblings sharing same id)
    targets: [],        // preferred: [{ id, selector: { thing_id } | null }] for bulk
    bulk: false,
    selector: null,
};

// ── Catalog helpers ───────────────────────────────────────────

function getExtraSystems() {
    const catalogIds = new Set((data?.catalogs?.systems ?? []).map(s => s.id));
    const extra = new Map();
    (data?.sensors ?? []).forEach(s => {
        if (s.system_id && !catalogIds.has(s.system_id) && !extra.has(s.system_id))
            extra.set(s.system_id, { id: s.system_id, name: s.system_name ?? s.system_id });
    });
    return [...extra.values()];
}

function allSystems() {
    return [
        ...(data?.catalogs?.systems ?? []).map(s => ({ value: s.id, label: `${s.id} — ${s.name}` })),
        ...getExtraSystems().map(s => ({ value: s.id, label: `${s.id} — ${s.name}` })),
    ];
}

function allNeighborhoods() {
    return (data?.catalogs?.neighborhoods ?? []).map(n => ({ value: n.key, label: n.name }));
}

function allDistricts() {
    return (data?.catalogs?.districts ?? []).map(d => ({ value: d.code, label: d.name }));
}

function allBuildings() {
    return (data?.buildings ?? []).map(b => ({
        value: b.id,
        label: `${b.id} — ${b.short_name || b.name || ''}`.trim(),
    }));
}

// ── Form field builders ───────────────────────────────────────

function dpReadonly(label, value) {
    return `<div class="dp-row">
        <label class="dp-label">${esc(label)}</label>
        <span class="dp-readonly">${esc(value ?? '—')}</span>
    </div>`;
}

function dpText(field, label, value) {
    return `<div class="dp-row">
        <label class="dp-label" for="dp-${field}">${esc(label)}</label>
        <input type="text" id="dp-${field}" data-field="${field}"
               class="dp-input" value="${esc(value ?? '')}">
    </div>`;
}

function dpNumber(field, label, value) {
    return `<div class="dp-row">
        <label class="dp-label" for="dp-${field}">${esc(label)}</label>
        <input type="number" id="dp-${field}" data-field="${field}"
               class="dp-input" step="any" value="${esc(value ?? '')}">
    </div>`;
}

function dpTextarea(field, label, value) {
    return `<div class="dp-row dp-row-tall">
        <label class="dp-label" for="dp-${field}">${esc(label)}</label>
        <textarea id="dp-${field}" data-field="${field}" class="dp-textarea" rows="3">${esc(value ?? '')}</textarea>
    </div>`;
}

function dpSelect(field, label, options, currentValue) {
    const opts = options.map(o =>
        `<option value="${esc(o.value)}"${o.value === currentValue ? ' selected' : ''}>${esc(o.label)}</option>`
    ).join('');
    return `<div class="dp-row">
        <label class="dp-label" for="dp-${field}">${esc(label)}</label>
        <select id="dp-${field}" data-field="${field}" class="dp-input">
            <option value="">—</option>${opts}
        </select>
    </div>`;
}

// ── Form rendering ────────────────────────────────────────────

function renderDetailForm(record, entityType) {
    const rows = [];
    if (entityType === 'sensor') {
        rows.push(dpReadonly('ID', record.id));
        rows.push(dpReadonly('Tipo', record.type));
        rows.push(dpSelect('system_id', 'Sistema', allSystems(), record.system_id));
        rows.push(dpSelect('neighborhood_key', 'Barrio', allNeighborhoods(), record.neighborhood_key));
        rows.push(dpSelect('district_code', 'Distrito', allDistricts(), record.district_code));
        rows.push(dpSelect('hos', 'Edificio HOS', allBuildings(), record.hos));
        rows.push(dpText('ref_etra', 'Calle', record.ref_etra));
        rows.push(dpNumber('lat', 'Latitud', record.lat));
        rows.push(dpNumber('lon', 'Longitud', record.lon));
        rows.push(dpText('thing_id', 'ThingID', record.thing_id));
        rows.push(dpText('thing_token', 'ThingToken', record.thing_token));
        rows.push(dpText('tags', 'Tags', record.tags ?? ''));
        rows.push(dpTextarea('observaciones', 'Observaciones', record.observaciones));
    } else {
        rows.push(dpReadonly('ID', record.id));
        rows.push(dpText('short_name', 'Nombre corto', record.short_name));
        rows.push(dpText('description', 'Descripción', record.description));
        rows.push(dpText('type', 'Tipo', record.type));
        rows.push(dpText('zone', 'Zona', record.zone));
        rows.push(dpSelect('neighborhood_key', 'Barrio', allNeighborhoods(), record.neighborhood_key));
        rows.push(dpSelect('district_code', 'Distrito', allDistricts(), record.district_code));
        rows.push(dpText('street_etra', 'Calle', record.street_etra));
        rows.push(dpNumber('lat', 'Latitud', record.lat));
        rows.push(dpNumber('lon', 'Longitud', record.lon));
        rows.push(dpText('thing_id', 'ThingID', record.thing_id));
        rows.push(dpText('thing_token', 'ThingToken', record.thing_token));
        rows.push(dpText('tags', 'Tags', record.tags ?? ''));
        rows.push(dpTextarea('observaciones', 'Observaciones', record.observaciones));
    }
    document.getElementById('dp-body').innerHTML = `<form id="dp-form">${rows.join('')}</form>`;

    const copyBtn = document.getElementById('dp-copy-btn');
    if (copyBtn) copyBtn.style.display = (entityType === 'sensor') ? '' : 'none';
    const pushSensorsBtn = document.getElementById('dp-push-sensors-btn');
    if (pushSensorsBtn) pushSensorsBtn.style.display = (entityType === 'building') ? '' : 'none';
}

function renderBulkForm(entityType) {
    const note = `<p class="dp-bulk-note">Los campos en blanco no se modificarán.</p>`;
    const rows = [note];
    if (entityType === 'sensor') {
        rows.push(dpSelect('system_id', 'Sistema', allSystems(), ''));
        rows.push(dpSelect('neighborhood_key', 'Barrio', allNeighborhoods(), ''));
        rows.push(dpSelect('district_code', 'Distrito', allDistricts(), ''));
        rows.push(dpSelect('hos', 'Edificio HOS', allBuildings(), ''));
    } else {
        rows.push(dpSelect('neighborhood_key', 'Barrio', allNeighborhoods(), ''));
        rows.push(dpSelect('district_code', 'Distrito', allDistricts(), ''));
        rows.push(dpText('type', 'Tipo', ''));
        rows.push(dpText('zone', 'Zona', ''));
    }
    document.getElementById('dp-body').innerHTML = `<form id="dp-form">${rows.join('')}</form>`;
    const copyBtn = document.getElementById('dp-copy-btn');
    if (copyBtn) copyBtn.style.display = 'none';
    const pushSensorsBtn = document.getElementById('dp-push-sensors-btn');
    if (pushSensorsBtn) pushSensorsBtn.style.display = 'none';
}

// ── Panel open / close ────────────────────────────────────────

function openDetailPanel(id, thingId = null) {
    if (!id) { closeDetailPanel(); return; }
    const isBuilding = !!data._buildingsMap[id];
    const entityType = isBuilding ? 'building' : 'sensor';
    const record = isBuilding
        ? data._buildingsMap[id]
        : findSensor(id, thingId);
    if (!record) return;

    editState.entityType = entityType;
    editState.ids = [id];
    editState.bulk = false;
    editState.selector = record.thing_id
        ? { thing_id: record.thing_id }
        : null;
    _pendingCopyChanges = null;

    document.getElementById('dp-title').textContent =
        `${entityType === 'building' ? 'Edificio' : 'Sensor'} ${id}`;
    renderDetailForm(record, entityType);

    const preview = document.getElementById('dp-copy-preview');
    if (preview) preview.style.display = 'none';

    const syncBtn = document.getElementById('dp-sync-btn');
    if (syncBtn) {
        const st = record._sync?.status;
        syncBtn.style.display = (st === 'pending' || st === 'error') ? '' : 'none';
        syncBtn.textContent   = st === 'error' ? '↑ Reintentar sync' : '↑ Sincronitzar';
    }

    document.getElementById('detail-panel').classList.add('open');
}

function openBulkEdit(type) {
    const isBuildingKey = key => !!(data._buildingsMap[key] || data._buildingsByThingId?.[key]);
    const keys = [...state.multiSelect].filter(key =>
        type === 'building' ? isBuildingKey(key) : !isBuildingKey(key)
    );
    if (!keys.length) return;

    const records = keys.map(key => getRecordByKey(key)?.record).filter(Boolean);
    const targets = records.map(r => ({
        id: r.id,
        selector: r.thing_id ? { thing_id: r.thing_id } : null,
    }));
    const ids = [...new Set(records.map(r => r.id))]; // compat only

    editState.entityType = type;
    editState.ids     = ids;
    editState.targets = targets;
    editState.bulk = true;
    editState.selector = null;
    _pendingCopyChanges = null;

    document.getElementById('dp-title').textContent =
        `Editar ${keys.length} ${type === 'building' ? 'edificios' : 'sensores'}`;
    renderBulkForm(type);

    const preview = document.getElementById('dp-copy-preview');
    if (preview) preview.style.display = 'none';

    document.getElementById('detail-panel').classList.add('open');
}

function closeDetailPanel() {
    document.getElementById('detail-panel').classList.remove('open');
    editState.entityType = null;
    editState.ids     = [];
    editState.targets = [];
    editState.bulk    = false;
    editState.selector = null;
    _pendingCopyChanges = null;
}

// ── Selection bar ─────────────────────────────────────────────

function renderSelectionBar() {
    const bar = document.getElementById('selection-bar');
    const card = document.getElementById('selected-building-card');
    if (!bar) return;
    const n = state.multiSelect.size;

    if (n > 1) {
        if (card) { card.classList.add('hidden'); card.innerHTML = ''; }
        const sc2 = document.getElementById('selected-sensor-card');
        if (sc2) { sc2.classList.add('hidden'); sc2.innerHTML = ''; }
        const type = state.multiSelectType;
        const label = type === 'building' ? 'edificios' : 'sensores';
        bar.innerHTML = `
            <div class="selection-info">
                <span class="selection-count">${n} ${label} seleccionados</span>
            </div>
            <div class="selection-actions">
                <button class="sel-btn" onclick="editSelectedRecord()">&#9999; Editar ${n}</button>
                <button class="sel-btn sel-btn-clear" onclick="clearSelection()">&#10005; Limpiar</button>
            </div>`;
        bar.style.display = 'flex';
        return;
    }

    // Multi-select (n===1): resolve actual id/thingId from the stored key
    if (n === 1) {
        const found = getRecordByKey([...state.multiSelect][0]);
        state.selectedId      = found?.record.id      || [...state.multiSelect][0];
        state.selectedThingId = found?.record.thing_id || null;
    }

    const sensorCard = document.getElementById('selected-sensor-card');
    bar.style.display = 'none';

    // No context at all
    if (!state.selectedBuildingId && !state.selectedSensorId) {
        if (card) { card.classList.add('hidden'); card.innerHTML = ''; }
        if (sensorCard) { sensorCard.classList.add('hidden'); sensorCard.innerHTML = ''; }
        bar.style.display = 'none';
        return;
    }

    // Render building card (always when there is a building context)
    if (state.selectedBuildingId && data._buildingsMap[state.selectedBuildingId]) {
        renderSelectedBuildingCard(data._buildingsMap[state.selectedBuildingId]);
    } else if (card) {
        card.classList.add('hidden'); card.innerHTML = '';
    }

    // Render sensor card (only when a sensor is active)
    if (state.selectedSensorId) {
        const s = findSensor(state.selectedSensorId, state.selectedSensorThingId);
        if (s) renderSelectedSensorCard(s);
        else if (sensorCard) { sensorCard.classList.add('hidden'); sensorCard.innerHTML = ''; }
    } else {
        if (sensorCard) { sensorCard.classList.add('hidden'); sensorCard.innerHTML = ''; }
    }
}

function renderSelectedBuildingCard(b) {
    const card = document.getElementById('selected-building-card');
    if (!card || !b) return;

    const sensors = data._sensorsByBuilding[b.id] ?? [];
    const systemIds = [...new Set(sensors.map(s => s.system_id).filter(Boolean))];
    const sysBadges = systemIds.map(sid =>
        `<span class="sys-badge" style="background:${esc(getSystemColor(sid))}" title="${esc(sid)}">${esc(sid)}</span>`
    ).join('');
    const meta = [b.type, b.neighborhood, b.district_name || b.district_code, b.state]
        .filter(Boolean).map(esc).join('<span class="meta-sep">·</span>');

    card.classList.remove('hidden');
    card.innerHTML = `
        <div class="selection-card-main">
            <div class="selection-card-icon">
                ${b.image ? `<img src="${esc(b.image)}" alt="">` : '<span class="card-icon-emoji">&#127970;</span>'}
            </div>
            <div class="selection-card-info">
                <div class="selection-card-kicker">Contexto actual</div>
                <div class="selection-card-title">${esc(b.id)} · ${esc(b.short_name || b.name || '')}</div>
                <div style="font-family:monospace;font-size:0.75em;margin-top:2px" title="${esc(b.thing_id ?? '')}">ThingID: <strong>${b.thing_id ? esc(truncate(b.thing_id, 20)) : '—'}</strong></div>
                <div class="selection-card-meta">${meta}</div>
                <div class="selection-card-systems">
                    ${sysBadges}
                    <span class="sys-count">${sensors.length} sensor${sensors.length !== 1 ? 'es' : ''}</span>
                    ${b.iot_health_status ? `<span class="iot-badge iot-${b.iot_health_status.toLowerCase()}">${b.iot_active_sensors ?? 0}/${b.iot_total_sensors ?? 0} IoT</span>` : ''}
                </div>
            </div>
            <div class="selection-card-actions">
                <button type="button" class="card-btn" onclick="editSelectedRecord()" title="Editar">&#9999;</button>
                <button type="button" class="card-btn" onclick="zoomSelectedRecord()" title="Zoom">&#128205;</button>
                <button type="button" class="card-btn card-btn-clear" onclick="clearSelection()" title="Limpiar">&#10005;</button>
            </div>
        </div>
    `;
}

function renderSelectedSensorCard(s) {
    const card = document.getElementById('selected-sensor-card');
    if (!card || !s) return;

    const color = getSystemColor(s.system_id);
    const meta = [s.system_name, s.type, s.ref_etra, s.neighborhood]
        .filter(Boolean).map(esc).join('<span class="meta-sep">·</span>');

    card.classList.remove('hidden');
    card.innerHTML = `
        <div class="selection-card-main">
            <div class="selection-card-icon">
                <div class="sys-icon-circle" style="background:${esc(color)}">${esc(s.system_id || '?')}</div>
            </div>
            <div class="selection-card-info">
                <div class="selection-card-kicker">Sensor activo${s.hos ? ` · HOS: ${esc(s.hos)}` : ''}</div>
                <div class="selection-card-title">${esc(s.id)}</div>
                <div style="font-family:monospace;font-size:0.75em;margin-top:2px" title="${esc(s.thing_id ?? '')}">ThingID: <strong>${s.thing_id ? esc(truncate(s.thing_id, 20)) : '—'}</strong></div>
                <div class="selection-card-meta">${meta}</div>
                <div class="selection-card-systems">
                    <span class="sys-badge" style="background:${esc(color)}">${esc(s.system_id || '')}</span>
                    ${s.iot_health
                        ? `<span class="iot-badge iot-${s.iot_health.demo_ready ? 'active' : 'nodata'}">${esc(s.iot_health.status)}</span>`
                        : `<span class="sys-count">${esc(s.has_data || '-')}</span>`}
                    ${s.iot_health?.last_seen ? `<span class="meta-sep">·</span><span class="sys-count">${esc(s.iot_health.last_seen.slice(0,10))}</span>` : ''}
                    ${s.district_name || s.district_code ? `<span class="meta-sep">·</span><span class="sys-count">${esc(s.district_name || s.district_code)}</span>` : ''}
                </div>
            </div>
            <div class="selection-card-actions">
                <button type="button" class="card-btn" onclick="editSelectedRecord()" title="Editar">&#9999;</button>
                <button type="button" class="card-btn" onclick="zoomSelectedRecord()" title="Zoom">&#128205;</button>
                <button type="button" class="card-btn card-btn-clear" onclick="clearSensor()" title="Cerrar sensor">&#10005;</button>
            </div>
        </div>
    `;
}

function clearSensor() {
    state.selectedSensorId      = null;
    state.selectedSensorThingId = null;
    state.selectedId            = state.selectedBuildingId;
    state.selectedThingId       = data._buildingsMap[state.selectedBuildingId]?.thing_id || null;
    document.querySelectorAll('tr.row-selected').forEach(r => r.classList.remove('row-selected'));
    clearMapHighlight();
    if (state.selectedBuildingId) {
        highlightMapRecord(state.selectedBuildingId, 'building');
        const bldRow = document.querySelector(`tr[data-rid="${CSS.escape(state.selectedBuildingId)}"]`);
        if (bldRow) { bldRow.classList.add('row-selected'); bldRow.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); }
    }
    closeDetailPanel();
    renderSelectionBar();
    renderSensorsList();
}

function clearSelection() {
    state.selectedId            = null;
    state.selectedThingId       = null;
    state.selectedBuildingId    = null;
    state.selectedSensorId      = null;
    state.selectedSensorThingId = null;
    document.querySelectorAll('tr.row-selected').forEach(r => r.classList.remove('row-selected'));
    clearMapHighlight();
    closeDetailPanel();
    clearMultiSelect();  // calls updateMultiSelectUI() → renderSelectionBar() → hides bar
    renderSensorsList();
}

function editSelectedRecord() {
    const n = state.multiSelect.size;
    if (n > 1) {
        openBulkEdit(state.multiSelectType);
    } else if (n === 1) {
        const found = getRecordByKey([...state.multiSelect][0]);
        if (found) openDetailPanel(found.record.id, found.record.thing_id || null);
    } else if (state.selectedSensorId) {
        openDetailPanel(state.selectedSensorId, state.selectedSensorThingId);
    } else if (state.selectedBuildingId) {
        openDetailPanel(state.selectedBuildingId);
    }
}

function zoomSelectedRecord() {
    const n = state.multiSelect.size;
    if (n === 1) {
        const found = getRecordByKey([...state.multiSelect][0]);
        if (found?.type === 'building') focusBuilding(found.record.id);
        else if (found) focusSensor(found.record.id, found.record.thing_id || null);
        return;
    }
    // Zoom to sensor if active, else to building context
    if (state.selectedSensorId) {
        focusSensor(state.selectedSensorId, state.selectedSensorThingId);
    } else if (state.selectedBuildingId) {
        focusBuilding(state.selectedBuildingId);
    }
}

// ── Save ──────────────────────────────────────────────────────

function getSingleFormValues() {
    const updates = {};
    document.querySelectorAll('#dp-form [data-field]').forEach(el => {
        const k = el.dataset.field;
        const v = el.value.trim();
        updates[k] = v || null;
    });
    return updates;
}

function getBulkFormValues() {
    const updates = {};
    document.querySelectorAll('#dp-form [data-field]').forEach(el => {
        const v = el.value.trim();
        if (v) updates[el.dataset.field] = v;
    });
    return updates;
}

async function saveDetailPanel() {
    const updates = editState.bulk ? getBulkFormValues() : getSingleFormValues();
    if (!updates || Object.keys(updates).length === 0) {
        showToast('No hay campos para guardar.', false);
        return;
    }

    // Capture state before async ops (may change on reloadData)
    const savedId         = editState.ids[0];
    const savedEntityType = editState.entityType;
    const savedBulk       = editState.bulk;
    const savedSelector   = editState.selector;
    const savedTargets    = editState.targets.slice();
    const savedTargetCount = savedBulk ? savedTargets.length : 1;

    try {
        let result;
        if (savedBulk) {
            result = await fetchJson('/api/save-batch', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    entityType: savedEntityType,
                    targets: savedTargets,
                    updates,
                }),
            });
        } else {
            result = await fetchJson('/api/save-record', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    entityType: savedEntityType,
                    id: savedId,
                    selector: savedSelector,
                    updates,
                }),
            });
        }

        if (!result.ok) throw new Error(result.error);

        await reloadData();

        let msg;
        if (savedBulk) {
            msg = `${savedTargetCount} registros guardados.`;
            if (result.records_updated > savedTargetCount) {
                msg = `${savedTargetCount} registros guardados (${result.records_updated} en total).`;
            }
        } else {
            msg = 'Guardado correctamente.';
            if (result.records?.length > 1) {
                msg = `Guardado correctamente (${result.records.length} sensores con el mismo ID actualizados).`;
            }
        }
        if (result.sensors_updated > 0) {
            msg += ` ${result.sensors_updated} sensor${result.sensors_updated === 1 ? '' : 'es'} del edificio actualizado${result.sensors_updated === 1 ? '' : 's'}.`;
        }
        showToast(msg, true);
        loadPushStatus();

        if (savedEntityType === 'building' && !savedBulk) {
            // Stay on building panel — re-render with fresh data
            openDetailPanel(savedId);
        } else {
            closeDetailPanel();
            clearMultiSelect();
        }

    } catch (err) {
        showToast('Error: ' + err.message, false);
    }
}

// ── Copy from building ────────────────────────────────────────

function showCopyFromBuilding() {
    const hosEl = document.getElementById('dp-hos');
    if (!hosEl || !hosEl.value) {
        showToast('El sensor no tiene edificio HOS asignado.', false);
        return;
    }
    const building = data._buildingsMap[hosEl.value];
    if (!building) { showToast('Edificio no encontrado.', false); return; }

    const sensor = findSensor(editState.ids[0], editState.selector?.thing_id);
    const FIELDS = [
        { key: 'neighborhood_key', label: 'Barrio' },
        { key: 'district_code', label: 'Distrito' },
        { key: 'street_etra', label: 'Calle' },
        { key: 'lat', label: 'Latitud' },
        { key: 'lon', label: 'Longitud' },
    ];

    _pendingCopyChanges = FIELDS
        .filter(f => building[f.key] != null)
        .map(f => ({ ...f, from: sensor?.[f.key] ?? null, to: building[f.key] }));

    if (!_pendingCopyChanges.length) {
        showToast('El edificio no tiene datos para copiar.', false);
        return;
    }

    const rows = _pendingCopyChanges.map(c => `
        <div class="dp-preview-row">
            <span class="dp-preview-label">${esc(c.label)}</span>
            <span class="dp-preview-old">${esc(c.from != null ? String(c.from) : 'VACÍO')}</span>
            <span class="dp-preview-arrow">→</span>
            <span class="dp-preview-new">${esc(String(c.to))}</span>
        </div>`).join('');

    const preview = document.getElementById('dp-copy-preview');
    preview.innerHTML = `
        <div class="dp-preview-title">Copiar datos del edificio</div>
        ${rows}
        <div class="dp-preview-btns">
            <button class="btn-pri" onclick="applyCopyFromBuilding()">Aplicar</button>
            <button class="btn-sec" onclick="cancelCopyFromBuilding()">Cancelar</button>
        </div>`;
    preview.style.display = 'block';
}

function applyCopyFromBuilding() {
    if (!_pendingCopyChanges) return;
    _pendingCopyChanges.forEach(c => {
        const el = document.getElementById('dp-' + c.key);
        if (el) el.value = c.to;
    });
    cancelCopyFromBuilding();
    showToast('Datos copiados. Pulsa Guardar para persistir.', true);
}

function cancelCopyFromBuilding() {
    _pendingCopyChanges = null;
    const preview = document.getElementById('dp-copy-preview');
    if (preview) preview.style.display = 'none';
}

// ── Push building data to all sensors ────────────────────────

const BUILDING_PUSH_FIELDS = [
    'district_code', 'district_name',
    'neighborhood_key', 'neighborhood',
    'type', 'zone',
    'street_etra', 'street_mti',
    'lat', 'lon',
];

let _pendingPushToSensors = null;

function pushBuildingToSensors() {
    const buildingId = editState.ids[0];
    if (!buildingId) return;

    // Form values take priority over saved data (user may have edited without saving yet)
    const formValues = getSingleFormValues();
    const saved      = data._buildingsMap[buildingId] || {};

    const pushValues = {};
    BUILDING_PUSH_FIELDS.forEach(f => {
        const v = (formValues[f] != null && formValues[f] !== '') ? formValues[f] : saved[f];
        if (v != null && v !== '') pushValues[f] = v;
    });

    if (!Object.keys(pushValues).length) {
        showToast('El edificio no tiene datos para propagar.', false);
        return;
    }

    const sensors = (data.sensors || []).filter(s => s.hos === buildingId);
    if (!sensors.length) {
        showToast('No hay sensores asociados a este edificio.', false);
        return;
    }

    // Store full form values for building save + push values for sensor propagation
    _pendingPushToSensors = { buildingId, formValues, pushValues, sensorCount: sensors.length };

    const rows = BUILDING_PUSH_FIELDS
        .filter(f => pushValues[f] != null)
        .map(f => `
        <div class="dp-preview-row">
            <span class="dp-preview-label">${esc(f)}</span>
            <span class="dp-preview-new">${esc(String(pushValues[f]))}</span>
        </div>`).join('');

    const preview = document.getElementById('dp-copy-preview');
    preview.innerHTML = `
        <div class="dp-preview-title">Guardar edificio y copiar a ${sensors.length} sensor${sensors.length === 1 ? '' : 'es'}</div>
        ${rows}
        <div class="dp-preview-btns">
            <button class="btn-pri" onclick="applyPushBuildingToSensors()">Guardar y propagar</button>
            <button class="btn-sec" onclick="cancelPushBuildingToSensors()">Cancelar</button>
        </div>`;
    preview.style.display = 'block';
}

async function applyPushBuildingToSensors() {
    if (!_pendingPushToSensors) return;
    const { buildingId, formValues, sensorCount } = _pendingPushToSensors;
    cancelPushBuildingToSensors();

    try {
        // Save building with current form values — server auto-propagates BUILDING_TO_SENSOR_FIELDS
        const result = await fetchJson('/api/save-record', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ entityType: 'building', id: buildingId, selector: null, updates: formValues }),
        });
        if (!result.ok) throw new Error(result.error);
        await reloadData();
        const n = result.sensors_updated ?? sensorCount;
        showToast(`Edificio guardado. ${n} sensor${n === 1 ? '' : 'es'} actualizados.`, true);
        loadPushStatus();
        openDetailPanel(buildingId);
    } catch (err) {
        showToast('Error: ' + err.message, false);
    }
}

function cancelPushBuildingToSensors() {
    _pendingPushToSensors = null;
    const preview = document.getElementById('dp-copy-preview');
    if (preview) preview.style.display = 'none';
}

// ── Multi-select ──────────────────────────────────────────────

function toggleMultiSelect(id, type) {
    if (state.multiSelectType && state.multiSelectType !== type)
        state.multiSelect.clear();
    state.multiSelectType = type;

    if (state.multiSelect.has(id)) {
        state.multiSelect.delete(id);
    } else {
        state.multiSelect.add(id);
        state.lastSelectedId = id;
    }
    if (!state.multiSelect.size) state.multiSelectType = null;
    updateMultiSelectUI();
}

function rangeMultiSelect(id, type, records) {
    if (state.multiSelectType && state.multiSelectType !== type)
        state.multiSelect.clear();
    state.multiSelectType = type;

    const keys = records.map(r => getRecordKey(r));
    const last = state.lastSelectedId ? keys.indexOf(state.lastSelectedId) : -1;
    const curr = keys.indexOf(id);
    if (last === -1) {
        state.multiSelect.add(id);
    } else {
        const [a, b] = [Math.min(last, curr), Math.max(last, curr)];
        for (let i = a; i <= b; i++) state.multiSelect.add(keys[i]);
    }
    updateMultiSelectUI();
}

function clearMultiSelect() {
    state.multiSelect.clear();
    state.multiSelectType = null;
    updateMultiSelectUI();
}

function updateMultiSelectUI() {
    const n = state.multiSelect.size;

    const isBuildingKey = key => !!(data._buildingsMap[key] || data._buildingsByThingId?.[key]);

    // Buildings bulk button
    const bldKeys = n > 0 ? [...state.multiSelect].filter(isBuildingKey) : [];
    const btnBld = document.getElementById('btn-bulk-bld');
    const cntBld = document.getElementById('bulk-count-bld');
    if (btnBld) { btnBld.style.display = bldKeys.length > 1 ? '' : 'none'; if (cntBld) cntBld.textContent = bldKeys.length; }

    // Sensors bulk button
    const snsKeys = n > 0 ? [...state.multiSelect].filter(k => !isBuildingKey(k)) : [];
    const btnSns = document.getElementById('btn-bulk-sns');
    const cntSns = document.getElementById('bulk-count-sns');
    if (btnSns) { btnSns.style.display = snsKeys.length > 1 ? '' : 'none'; if (cntSns) cntSns.textContent = snsKeys.length; }

    // Row classes — compare against data-key (thing_id || id), not data-rid (id only)
    document.querySelectorAll('tr[data-key]').forEach(tr => {
        tr.classList.toggle('row-multi-selected', state.multiSelect.has(tr.dataset.key));
    });

    renderSelectionBar();
}

// ── API Import / Sync ─────────────────────────────────────────

let _syncPollTimer = null;

async function importFromAPI() {
    const btn = document.getElementById('btn-sync');
    btn.disabled = true;
    try {
        const result = await fetchJson('/api/import', { method: 'POST' });
        _pollSyncStatus();
    } catch (err) {
        showToast('Error al iniciar: ' + err.message, false);
        btn.disabled = false;
    }
}

function _pollSyncStatus() {
    clearTimeout(_syncPollTimer);
    _syncPollTimer = setTimeout(async () => {
        try {
            const s = await fetchJson('/api/import-status');
            _updateSyncUI(s);
            if (s.running) {
                _pollSyncStatus();
            } else {
                document.getElementById('btn-sync').disabled = false;
                if (s.done) {
                    await reloadData();
                    loadPushStatus();
                    if (s.inventory_health_skipped) {
                        const reason = s.inventory_stats?.reason || 'motivo desconocido';
                        showToast(`Sync completa: ${s.buildings} edif., ${s.sensors} sens. ⚠ Inventario IoT omitido: ${reason}`, false);
                    } else {
                        const warns = (s.warnings || []).length;
                        const warnTxt = warns > 0 ? ` · ${warns} aviso${warns > 1 ? 's' : ''}` : '';
                        showToast(`Sincronización completa: ${s.buildings} edificios, ${s.sensors} sensores${warnTxt}.`, true);
                    }
                } else if (s.error) {
                    showToast('Error en sincronización: ' + s.error, false);
                }
            }
        } catch (e) {
            document.getElementById('btn-sync').disabled = false;
        }
    }, 1500);
}

function _updateSyncUI(s) {
    const el = document.getElementById('sync-status');
    if (!el) return;
    if (s.running) {
        const phase = s.phase || 'importing';
        if (phase === 'resolving_tags') {
            el.textContent = 'Resolviendo tags automáticamente…';
        } else if (phase === 'updating_inventory') {
            el.textContent = s.sub_status || 'Actualizando inventario IoT…';
        } else {
            el.textContent = `Importando… ${s.things_done} things · ${s.current_model}`;
        }
    } else if (s.done && s.finished_at) {
        const t = new Date(s.finished_at).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
        el.textContent = `Sync ${t} · ${s.buildings} edif. ${s.sensors} sens.`;
    } else {
        el.textContent = '';
    }
}

// ── Resolve Tags Modal ────────────────────────────────────────

let _resolvePollTimer = null;

function openResolveModal() {
    document.getElementById('resolve-modal').style.display = 'flex';
}
function closeResolveModal() {
    document.getElementById('resolve-modal').style.display = 'none';
}

async function resolveTagsFromAPI() {
    const btn = document.getElementById('btn-resolve');
    btn.disabled = true;
    openResolveModal();

    const logEl = document.getElementById('resolve-log');
    logEl.innerHTML = '';
    document.getElementById('resolve-progress-bar').style.width = '0%';
    document.getElementById('resolve-summary').textContent = '';
    document.getElementById('resolve-close-btn').disabled = true;

    _addResolveLog('Iniciando resolución de tags…', 'dim');

    try {
        await fetchJson('/api/resolve-tags', { method: 'POST' });
        _pollResolveStatus(0);
    } catch (err) {
        _addResolveLog('Error: ' + err.message, 'err');
        document.getElementById('resolve-close-btn').disabled = false;
        btn.disabled = false;
    }
}

function _pollResolveStatus(lastCount) {
    clearTimeout(_resolvePollTimer);
    _resolvePollTimer = setTimeout(async () => {
        try {
            const s = await fetchJson('/api/resolve-status');
            const log = s.log || [];

            for (let i = lastCount; i < log.length; i++) {
                const msg = log[i];
                const cls = msg.startsWith('✓') ? 'ok' : msg.startsWith('Error') ? 'err' : '';
                _addResolveLog(msg, cls);
            }

            const pct = s.total > 0 ? Math.round((s.done_count / s.total) * 100) : 0;
            document.getElementById('resolve-progress-bar').style.width = pct + '%';

            if (s.running) {
                _pollResolveStatus(log.length);
            } else {
                document.getElementById('resolve-close-btn').disabled = false;
                document.getElementById('btn-resolve').disabled = false;
                if (s.done) {
                    document.getElementById('resolve-progress-bar').style.width = '100%';
                    _renderResolveSummary(s);
                    await reloadData();
                    showToast(`Tags resueltos: ${s.buildings_updated} edificios, ${s.sensors_updated} sensores.`, true);
                } else if (s.error) {
                    _addResolveLog('Error: ' + s.error, 'err');
                }
            }
        } catch (e) {
            _addResolveLog('Error de conexión: ' + e.message, 'err');
            document.getElementById('resolve-close-btn').disabled = false;
            document.getElementById('btn-resolve').disabled = false;
        }
    }, 1000);
}

function _renderResolveSummary(s) {
    const el = document.getElementById('resolve-summary');
    if (!el) return;
    let dur = '';
    if (s.started_at && s.finished_at) {
        const ms = new Date(s.finished_at) - new Date(s.started_at);
        dur = ` · ${(ms / 1000).toFixed(1)}s`;
    }
    const fc  = s.fields_count  || {};
    const unk = s.tags_unknown  || [];
    let html = `<div class="rsb">`;
    html += `<div class="rsb-title">Resumen${dur}</div>`;
    html += `<div class="rsb-grid">`;
    html += `<div class="rsb-col">`;
    html += `<div class="rsb-section">Edificios (${s.total})</div>`;
    html += `<div class="rsb-row rsb-ok">✓ Resueltos: <strong>${s.buildings_updated}</strong></div>`;
    html += `<div class="rsb-row rsb-warn">⚠ Sin coincidencia: <strong>${s.skipped || 0}</strong></div>`;
    html += `<div class="rsb-row rsb-dim">○ Sin tags: <strong>${s.no_tags || 0}</strong></div>`;
    html += `</div>`;
    html += `<div class="rsb-col">`;
    html += `<div class="rsb-section">Campos aplicados</div>`;
    html += `<div class="rsb-row">Distrito: <strong>${fc.district_code || 0}</strong></div>`;
    html += `<div class="rsb-row">Barrio: <strong>${fc.neighborhood_key || 0}</strong></div>`;
    html += `<div class="rsb-row">Tipo: <strong>${fc.type || 0}</strong></div>`;
    html += `<div class="rsb-row">Zona: <strong>${fc.zone || 0}</strong></div>`;
    html += `<div class="rsb-row">Calle: <strong>${fc.street_etra || 0}</strong></div>`;
    html += `</div>`;
    html += `</div>`;
    html += `<div class="rsb-sensors">Sensores actualizados: <strong>${s.sensors_updated}</strong>`;
    if (s.sensors_no_building) html += ` · sin edificio asignado: <strong>${s.sensors_no_building}</strong>`;
    html += `</div>`;
    if (unk.length > 0) {
        html += `<div class="rsb-unknown">Tags no reconocidos (${unk.length}): <span class="rsb-tags">${unk.join(', ')}</span></div>`;
    }
    html += `</div>`;
    el.innerHTML = html;
}

function _addResolveLog(msg, cls = '') {
    const el = document.getElementById('resolve-log');
    if (!el) return;
    const line = document.createElement('div');
    line.className = cls ? `modal-log-${cls}` : '';
    line.textContent = msg;
    el.appendChild(line);
    el.scrollTop = el.scrollHeight;
}

function _applyMetaSync(meta) {
    if (!meta?.last_sync) return;
    const d = new Date(meta.last_sync);
    const label = d.toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit' })
                + ' ' + d.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
    const el = document.getElementById('sync-status');
    if (el && !el.textContent.startsWith('Import')) {
        el.textContent = `Sync ${label} · ${meta.buildings ?? ''} edif. ${meta.sensors ?? ''} sens.`;
    }
}

// Comprueba al arrancar si hay un import en curso (p.ej. tras recargar la página)
async function _checkSyncOnLoad() {
    try {
        const s = await fetchJson('/api/import-status');
        _updateSyncUI(s);
        if (s.running) {
            document.getElementById('btn-sync').disabled = true;
            _pollSyncStatus();
        }
    } catch { /* silencioso */ }
}

// ── Toast ─────────────────────────────────────────────────────

function showToast(msg, ok = true) {
    const el = document.getElementById('toast');
    if (!el) return;
    el.textContent = msg;
    el.className = 'toast ' + (ok ? 'toast-ok' : 'toast-err');
    el.style.display = 'block';
    clearTimeout(el._t);
    el._t = setTimeout(() => { el.style.display = 'none'; }, 3500);
}

// ── Push canvis a TheThings ────────────────────────────────────

async function loadPushStatus() {
    try {
        const s = await fetchJson('/api/sync-status');
        renderPushStatus(s);
    } catch { /* silencioso */ }
}

function renderPushStatus(s) {
    const el  = document.getElementById('push-status');
    const btn = document.getElementById('btn-push');
    if (!el || !btn) return;
    const pending = s.pending || 0;
    const errors  = s.errors  || 0;
    if (pending > 0) {
        el.textContent = `${pending} pendent${pending !== 1 ? 's' : ''} de pujar`;
        el.className   = 'push-status push-pending';
    } else if (errors > 0) {
        el.textContent = `${errors} error${errors !== 1 ? 's' : ''} de sync`;
        el.className   = 'push-status push-error';
    } else if (s.synced > 0) {
        el.textContent = 'Tot sincronitzat';
        el.className   = 'push-status push-synced';
    } else {
        el.textContent = '';
        el.className   = 'push-status';
    }
    btn.disabled = false;
}

async function syncAllPending() {
    const btn = document.getElementById('btn-push');
    const el  = document.getElementById('push-status');
    if (btn) btn.disabled = true;
    if (el)  { el.textContent = 'Pujant…'; el.className = 'push-status'; }
    try {
        const result = await fetchJson('/api/sync-all', { method: 'POST' });
        if (result.total === 0) {
            showToast('No hi ha canvis pendents de pujar.', true);
        } else {
            const msg = `Pujat: ${result.synced} ok, ${result.errors} errors de ${result.total}.`;
            showToast(msg, result.errors === 0);
        }
        await loadPushStatus();
    } catch (err) {
        showToast('Error sync: ' + err.message, false);
        await loadPushStatus();
    }
}

async function syncSelectedRecord() {
    const syncBtn = document.getElementById('dp-sync-btn');
    if (syncBtn) syncBtn.disabled = true;
    try {
        const result = await fetchJson('/api/sync-record', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                entityType: editState.entityType,
                id: editState.ids[0],
                selector: editState.selector,
            }),
        });
        if (result.result?.skipped) {
            showToast('Sense camps sync pendents.', true);
        } else {
            showToast(`Sincronitzat (${result.result?.values_sent ?? 0} camps).`, true);
        }
        await reloadData();
        await loadPushStatus();
        if (syncBtn) syncBtn.style.display = 'none';
    } catch (err) {
        showToast('Error sync: ' + err.message, false);
        if (syncBtn) syncBtn.disabled = false;
    }
}
