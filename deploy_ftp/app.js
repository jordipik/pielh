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
    selectedId: null,
    onlyVisibleBld: false,
    onlyVisibleSns: false,
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
        const res = await fetch('pielh_qa_master.json');
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
}

// ── Normalize / index data ───────────────────────────────────

function normalizeData() {
    data._systemsMap = {};
    (data.catalogs?.systems ?? []).forEach(s => { data._systemsMap[s.id] = s; });

    data._buildingsMap = {};
    (data.buildings ?? []).forEach(b => { data._buildingsMap[b.id] = b; });

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
        return true;
    });

    filtered.sensors = (data.sensors ?? []).filter(s => {
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
        return true;
    });

    filtered.otherObjects = (data.other_objects ?? []).filter(o => {
        if (!search) return true;
        const hay = [o.id, o.name, o.group, o.object_type, o.thing_id]
            .filter(Boolean).join(' ').toLowerCase();
        return hay.includes(search);
    });

    renderMarkers();
    renderSummary();
    renderBuildingsList();
    renderSensorsList();
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
    if (hasData === 'OK') statusCls = 'bm-ok';
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
    marker.on('click', () => selectRecord(b.id, { source: 'map' }));
    layers.buildings.addLayer(marker);
    markerIndex.buildings[b.id] = marker;
}

// ── Sensor markers (circleMarker, colored by system) ─────────

function renderSensorMarker(s, offsets) {
    const pos = offsets[s.id];
    if (!pos) return;

    const color = getSystemColor(s.system_id);

    const marker = L.circleMarker([pos.lat, pos.lon], {
        pane: 'sensorsPane',
        radius: 6,
        fillColor: color,
        color: '#fff',
        weight: 1.5,
        fillOpacity: 0.9,
    });

    marker.on('click', () => selectRecord(s.id, { source: 'map' }));
    layers.sensors.addLayer(marker);
    markerIndex.sensors[s.id] = marker;
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

// ── Summary cards ────────────────────────────────────────────

function renderSummary() {
    document.getElementById('count-buildings').textContent = filtered.buildings.length;
    document.getElementById('count-sensors').textContent = filtered.sensors.length;
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
        if (b.id === state.selectedId) tr.classList.add('row-selected');
        if (b.state === 'Fuera Proyecto') tr.classList.add('row-fuera');
        tr.innerHTML = `
            <td title="${esc(b.id)}">${esc(b.id)}</td>
            <td title="${esc(b.name)}">${esc(truncate(b.name || b.short_name, 30))}</td>
            <td title="${esc(b.type)}">${esc(b.type ?? '—')}</td>
            <td title="${esc(b.neighborhood)}">${esc(shortNeighborhood(b.neighborhood))}</td>
            <td title="${esc(b.district_name)}">${esc(b.district_name ?? '—')}</td>
            <td title="${esc(b.street_etra)}">${esc(truncate(b.street_etra, 20))}</td>
            <td>${sCount}</td>
            <td style="color:${dataColor};font-weight:600">${esc(b.has_data ?? '—')}</td>
        `;
        tr.addEventListener('click', e => {
            if (e.ctrlKey || e.metaKey) {
                toggleMultiSelect(b.id, 'building');
            } else if (e.shiftKey && state.lastSelectedId) {
                rangeMultiSelect(b.id, 'building', _lastBuildingRecords);
            } else {
                clearMultiSelect();
                selectRecord(b.id, { source: 'table' });
            }
        });
        tbody.appendChild(tr);
    });
}

// ── Sensors list ─────────────────────────────────────────────

const SENSOR_LIMIT = 500;

function renderSensorsList() {
    let records = filtered.sensors;
    const selBldId = state.selectedId && data._buildingsMap[state.selectedId] ? state.selectedId : null;
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
        const tr = document.createElement('tr');
        tr.dataset.rid = s.id;
        if (s.id === state.selectedId) tr.classList.add('row-selected');
        tr.innerHTML = `
            <td title="${esc(s.id)}">${esc(truncate(s.id, 18))}</td>
            <td>${esc(s.hos ?? '—')}</td>
            <td title="${esc(s.system_name)}">
                <span class="sys-dot" style="background:${color}"></span>${esc(s.system_id ?? '—')}
            </td>
            <td title="${esc(s.neighborhood)}">${esc(shortNeighborhood(s.neighborhood))}</td>
            <td title="${esc(s.ref_etra)}">${esc(truncate(s.ref_etra, 18))}</td>
            <td style="color:${dataColor};font-weight:600">${esc(s.has_data ?? '—')}</td>
        `;
        tr.addEventListener('click', e => {
            if (e.ctrlKey || e.metaKey) {
                toggleMultiSelect(s.id, 'sensor');
            } else if (e.shiftKey && state.lastSelectedId) {
                rangeMultiSelect(s.id, 'sensor', _lastSensorRecords);
            } else {
                clearMultiSelect();
                selectRecord(s.id, { source: 'table' });
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

function focusSensor(id) {
    const s = (data.sensors ?? []).find(x => x.id === id);
    if (!s) return;
    const lat = getLat(s), lon = getLon(s);
    if (lat == null) return;

    if (!map.hasLayer(layers.sensors)) map.addLayer(layers.sensors);
    map.setView([lat, lon], 17, { animate: true });
}

// ── Map highlight ─────────────────────────────────────────────

function clearMapHighlight() {
    if (_hlLayer) { map.removeLayer(_hlLayer); _hlLayer = null; }
}

function highlightMapRecord(id, type) {
    clearMapHighlight();
    const m = type === 'building' ? markerIndex.buildings[id] : markerIndex.sensors[id];
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
    const { source = 'table' } = opts;

    document.querySelectorAll('tr.row-selected').forEach(r => r.classList.remove('row-selected'));
    clearMapHighlight();
    state.selectedId = id;
    if (!id) return;

    // Highlight row and scroll to it
    const row = document.querySelector(`tr[data-rid="${CSS.escape(id)}"]`);
    if (row) {
        row.classList.add('row-selected');
        row.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }

    const isBuilding = !!data._buildingsMap[id];
    if (isBuilding) {
        highlightMapRecord(id, 'building');
        if (source === 'map') {
            // Switch to buildings tab if not active
            const btn = document.querySelector('[data-tab="tab-buildings"]');
            if (btn && !document.getElementById('tab-buildings').classList.contains('active'))
                showTab(btn, 'tab-buildings');
        }
    } else {
        const s = (data.sensors ?? []).find(x => x.id === id);
        if (s) {
            highlightMapRecord(id, 'sensor');
            if (source === 'map') {
                const btn = document.querySelector('[data-tab="tab-sensors"]');
                if (btn && !document.getElementById('tab-sensors').classList.contains('active'))
                    showTab(btn, 'tab-sensors');
            }
        }
    }

    renderSelectionBar();
    if (isBuilding) renderSensorsList();
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
    document.getElementById('chk-visible-sns').addEventListener('change', e => {
        state.onlyVisibleSns = e.target.checked;
        renderSensorsList();
    });

    initResizableColumns('buildings-table');
    initResizableColumns('sensors-table');
    initPanelResizer();
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
    ids: [],     // single or bulk
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
        rows.push(dpText('short_name', 'Nombre corto', record.short_name));
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
        rows.push(dpTextarea('observaciones', 'Observaciones', record.observaciones));
    }
    document.getElementById('dp-body').innerHTML = `<form id="dp-form">${rows.join('')}</form>`;

    const copyBtn = document.getElementById('dp-copy-btn');
    if (copyBtn) copyBtn.style.display = (entityType === 'sensor') ? '' : 'none';
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
}

// ── Panel open / close ────────────────────────────────────────

function openDetailPanel(id) {
    if (!id) { closeDetailPanel(); return; }
    const isBuilding = !!data._buildingsMap[id];
    const entityType = isBuilding ? 'building' : 'sensor';
    const record = isBuilding
        ? data._buildingsMap[id]
        : (data.sensors ?? []).find(s => s.id === id);
    if (!record) return;

    editState.entityType = entityType;
    editState.ids = [id];
    editState.bulk = false;
    editState.selector = entityType === 'sensor' && record.thing_id
        ? { thing_id: record.thing_id }
        : null;
    _pendingCopyChanges = null;

    document.getElementById('dp-title').textContent =
        `${entityType === 'building' ? 'Edificio' : 'Sensor'} ${id}`;
    renderDetailForm(record, entityType);

    const preview = document.getElementById('dp-copy-preview');
    if (preview) preview.style.display = 'none';

    document.getElementById('detail-panel').classList.add('open');
}

function openBulkEdit(type) {
    const ids = [...state.multiSelect].filter(id =>
        type === 'building' ? !!data._buildingsMap[id] : !data._buildingsMap[id]
    );
    if (!ids.length) return;

    editState.entityType = type;
    editState.ids = ids;
    editState.bulk = true;
    editState.selector = null;
    _pendingCopyChanges = null;

    document.getElementById('dp-title').textContent =
        `Editar ${ids.length} ${type === 'building' ? 'edificios' : 'sensores'}`;
    renderBulkForm(type);

    const preview = document.getElementById('dp-copy-preview');
    if (preview) preview.style.display = 'none';

    document.getElementById('detail-panel').classList.add('open');
}

function closeDetailPanel() {
    document.getElementById('detail-panel').classList.remove('open');
    editState.entityType = null;
    editState.ids = [];
    editState.bulk = false;
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

    const id = n === 1 ? [...state.multiSelect][0] : state.selectedId;
    if (!id) {
        bar.style.display = 'none';
        if (card) { card.classList.add('hidden'); card.innerHTML = ''; }
        const sc = document.getElementById('selected-sensor-card');
        if (sc) { sc.classList.add('hidden'); sc.innerHTML = ''; }
        return;
    }

    const sensorCard = document.getElementById('selected-sensor-card');
    bar.style.display = 'none';

    const isBuilding = !!data._buildingsMap[id];
    if (isBuilding) {
        if (sensorCard) { sensorCard.classList.add('hidden'); sensorCard.innerHTML = ''; }
        renderSelectedBuildingCard(data._buildingsMap[id]);
    } else {
        const s = (data.sensors ?? []).find(x => x.id === id);
        const building = s && s.hos ? data._buildingsMap[s.hos] : null;
        if (building) {
            renderSelectedBuildingCard(building);
        } else if (card) {
            card.classList.add('hidden'); card.innerHTML = '';
        }
        if (s) renderSelectedSensorCard(s);
        else if (sensorCard) { sensorCard.classList.add('hidden'); sensorCard.innerHTML = ''; }
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
                <div class="selection-card-kicker">Edificio seleccionado</div>
                <div class="selection-card-title">${esc(b.id)} · ${esc(b.short_name || b.name || '')}</div>
                <div class="selection-card-meta">${meta}</div>
                <div class="selection-card-systems">
                    ${sysBadges}
                    <span class="sys-count">${sensors.length} sensor${sensors.length !== 1 ? 'es' : ''}</span>
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
                <div class="selection-card-kicker">Sensor seleccionado</div>
                <div class="selection-card-title">${esc(s.id)}</div>
                <div class="selection-card-meta">${meta}</div>
                <div class="selection-card-systems">
                    <span class="sys-badge" style="background:${esc(color)}">${esc(s.system_id || '')}</span>
                    <span class="sys-count">${esc(s.has_data || '-')}</span>
                    ${s.district_name || s.district_code ? `<span class="meta-sep">·</span><span class="sys-count">${esc(s.district_name || s.district_code)}</span>` : ''}
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

function clearSelection() {
    state.selectedId = null;
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
    } else {
        const id = n === 1 ? [...state.multiSelect][0] : state.selectedId;
        if (id) openDetailPanel(id);
    }
}

function zoomSelectedRecord() {
    const n = state.multiSelect.size;
    const id = n === 1 ? [...state.multiSelect][0] : state.selectedId;
    if (!id) return;
    if (data._buildingsMap[id]) focusBuilding(id);
    else focusSensor(id);
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

    try {
        let result;
        if (editState.bulk) {
            result = await fetchJson('/api/save-batch', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    entityType: editState.entityType,
                    ids: editState.ids,
                    updates,
                }),
            });
        } else {
            result = await fetchJson('/api/save-record', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    entityType: editState.entityType,
                    id: editState.ids[0],
                    selector: editState.selector,
                    updates,
                }),
            });
        }

        if (!result.ok) throw new Error(result.error);
        const persistedUpdates = result.updates ?? updates;

        // Update in-memory data
        editState.ids.forEach(id =>
            updateLocalRecord(editState.entityType, id, persistedUpdates, editState.selector)
        );

        // Refresh popup if open
        if (!editState.bulk) {
            const id = editState.ids[0];
            const marker = editState.entityType === 'building'
                ? markerIndex.buildings[id]
                : markerIndex.sensors[id];
            if (marker && marker.isPopupOpen()) {
                if (editState.entityType === 'building') {
                    const b = data._buildingsMap[id];
                    const sCount = (data._sensorsByBuilding[b.id] ?? []).length;
                    marker.setPopupContent(buildingPopup(b, sCount));
                } else {
                    const s = (data.sensors ?? []).find(x => x.id === id);
                    if (s) marker.setPopupContent(sensorPopup(s));
                }
            }
        }

        showToast(editState.bulk
            ? `${editState.ids.length} registros guardados.`
            : 'Guardado correctamente.', true);

        closeDetailPanel();
        clearMultiSelect();
        applyFilters();

    } catch (err) {
        showToast('Error: ' + err.message, false);
    }
}

function updateLocalRecord(entityType, id, updates, selector = null) {
    if (entityType === 'sensor') {
        const s = (data.sensors ?? []).find(x =>
            x.id === id && (!selector?.thing_id || x.thing_id === selector.thing_id)
        );
        if (!s) return;
        if ('hos' in updates && updates.hos !== s.hos) {
            // Re-index _sensorsByBuilding
            if (s.hos && data._sensorsByBuilding[s.hos]) {
                data._sensorsByBuilding[s.hos] = data._sensorsByBuilding[s.hos].filter(x => x.id !== id);
            }
            Object.assign(s, updates);
            if (s.hos) {
                if (!data._sensorsByBuilding[s.hos]) data._sensorsByBuilding[s.hos] = [];
                if (!data._sensorsByBuilding[s.hos].find(x => x.id === id))
                    data._sensorsByBuilding[s.hos].push(s);
            }
        } else {
            Object.assign(s, updates);
        }
    } else {
        const b = data._buildingsMap[id];
        if (b) Object.assign(b, updates);
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

    const sensor = (data.sensors ?? []).find(s => s.id === editState.ids[0]);
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

    const ids = records.map(r => r.id);
    const last = state.lastSelectedId ? ids.indexOf(state.lastSelectedId) : -1;
    const curr = ids.indexOf(id);
    if (last === -1) {
        state.multiSelect.add(id);
    } else {
        const [a, b] = [Math.min(last, curr), Math.max(last, curr)];
        for (let i = a; i <= b; i++) state.multiSelect.add(ids[i]);
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

    // Buildings bulk button
    const bldIds = n > 0 ? [...state.multiSelect].filter(id => !!data._buildingsMap[id]) : [];
    const btnBld = document.getElementById('btn-bulk-bld');
    const cntBld = document.getElementById('bulk-count-bld');
    if (btnBld) { btnBld.style.display = bldIds.length > 1 ? '' : 'none'; if (cntBld) cntBld.textContent = bldIds.length; }

    // Sensors bulk button
    const snsIds = n > 0 ? [...state.multiSelect].filter(id => !data._buildingsMap[id]) : [];
    const btnSns = document.getElementById('btn-bulk-sns');
    const cntSns = document.getElementById('bulk-count-sns');
    if (btnSns) { btnSns.style.display = snsIds.length > 1 ? '' : 'none'; if (cntSns) cntSns.textContent = snsIds.length; }

    // Row classes
    document.querySelectorAll('tr[data-rid]').forEach(tr => {
        tr.classList.toggle('row-multi-selected', state.multiSelect.has(tr.dataset.rid));
    });

    renderSelectionBar();
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
