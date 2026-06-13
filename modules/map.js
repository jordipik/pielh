// map.js — capa Leaflet
const MapView = (() => {
  let _map = null;
  let _layers = {};
  let _selectedMarker = null;
  let _onSelect = null;

  function init(containerId) {
    _map = L.map(containerId, { center: [41.362, 2.110], zoom: 14 });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 19
    }).addTo(_map);

    _layers = {
      buildings:     L.layerGroup().addTo(_map),
      sensors:       L.layerGroup(),
      neighborhoods: L.layerGroup(),
      districts:     L.layerGroup()
    };
  }

  function onSelect(fn) { _onSelect = fn; }

  function _clear(type) { _layers[type] && _layers[type].clearLayers(); }

  function _showOnly(...types) {
    ['buildings','sensors','neighborhoods','districts'].forEach(t => {
      if (types.includes(t)) {
        if (!_map.hasLayer(_layers[t])) _map.addLayer(_layers[t]);
      } else {
        if (_map.hasLayer(_layers[t])) _map.removeLayer(_layers[t]);
      }
    });
  }

  function _fireSelect(type, item) {
    if (_onSelect) _onSelect(type, item);
  }

  function _setSelected(marker) {
    if (_selectedMarker && _selectedMarker._icon)
      _selectedMarker._icon.classList.remove('marker-selected');
    _selectedMarker = marker;
    if (marker && marker._icon)
      marker._icon.classList.add('marker-selected');
  }

  // ── Buildings ────────────────────────────────────────────────
  function renderBuildings(buildings) {
    _clear('buildings');
    buildings.forEach(b => {
      if (!b.lat || !b.lon) return;
      const m = L.marker([b.lat, b.lon], { icon: _buildingIcon() });
      m._pielh = { type: 'buildings', item: b };
      m.on('click', () => { _setSelected(m); _fireSelect('buildings', b); });
      m.addTo(_layers.buildings);
    });
    _showOnly('buildings');
  }

  function _buildingIcon() {
    return L.divIcon({ className: 'map-bld', iconSize: [12, 12], iconAnchor: [6, 6] });
  }

  // ── Sensors ──────────────────────────────────────────────────
  function renderSensors(sensors, buildings) {
    _clear('sensors');

    // Group by rounded coordinates to spread overlapping markers
    const groups = {};
    sensors.forEach(s => {
      if (!s.lat || !s.lon) return;
      const key = `${s.lat.toFixed(4)},${s.lon.toFixed(4)}`;
      (groups[key] = groups[key] || []).push(s);
    });

    Object.values(groups).forEach(grp => {
      grp.forEach((s, i) => {
        const [dlat, dlon] = _spiralOffset(i, grp.length);
        const color = Data.getSystemColor(s.system_id);
        const icon = L.divIcon({
          className: 'map-sensor',
          html: `<div class="sensor-dot" style="background:${color}"></div>`,
          iconSize: [10, 10], iconAnchor: [5, 5]
        });
        const m = L.marker([s.lat + dlat, s.lon + dlon], { icon });
        m._pielh = { type: 'sensors', item: s };
        m.on('click', () => { _setSelected(m); _fireSelect('sensors', s); });
        m.addTo(_layers.sensors);
      });
    });

    // Always show buildings as background when viewing sensors
    if (buildings) renderBuildingsBg(buildings);
    _showOnly('buildings', 'sensors');
  }

  function renderBuildingsBg(buildings) {
    _clear('buildings');
    buildings.forEach(b => {
      if (!b.lat || !b.lon) return;
      const m = L.marker([b.lat, b.lon], { icon: _buildingIcon() });
      m._pielh = { type: 'buildings', item: b };
      m.on('click', () => { _setSelected(m); _fireSelect('buildings', b); });
      m.addTo(_layers.buildings);
    });
  }

  function _spiralOffset(i, total) {
    if (total <= 1 || i === 0) return [0, 0];
    const angle = (i / total) * 2 * Math.PI;
    const r = 0.00005;
    return [Math.sin(angle) * r, Math.cos(angle) * r];
  }

  // ── Neighborhoods ─────────────────────────────────────────────
  function renderNeighborhoods(neighborhoods) {
    _clear('neighborhoods');
    neighborhoods.forEach(n => {
      if (!n.lat || !n.lon) return;
      const circle = L.circleMarker([n.lat, n.lon], {
        radius: 22, color: '#3b82f6', weight: 2,
        fillColor: '#93c5fd', fillOpacity: 0.2
      });
      circle._pielh = { type: 'neighborhoods', item: n };
      circle.on('click', () => { _fireSelect('neighborhoods', n); });

      const label = L.marker([n.lat, n.lon], {
        icon: L.divIcon({
          className: 'map-label neigh-label',
          html: n.name, iconAnchor: [-4, 24]
        }),
        interactive: false
      });
      circle.addTo(_layers.neighborhoods);
      label.addTo(_layers.neighborhoods);
    });
    _showOnly('neighborhoods');
  }

  // ── Districts ─────────────────────────────────────────────────
  function renderDistricts(districts) {
    _clear('districts');
    districts.forEach(d => {
      // Use centroid from neighborhoods of this district
      const neigh = Data.getNeighborhoods().filter(n => n.district_code === d.code);
      const lat = neigh.length ? neigh.reduce((a, n) => a + n.lat, 0) / neigh.length : 41.362;
      const lon = neigh.length ? neigh.reduce((a, n) => a + n.lon, 0) / neigh.length : 2.11;

      const circle = L.circleMarker([lat, lon], {
        radius: 36, color: '#7c3aed', weight: 3,
        fillColor: '#c4b5fd', fillOpacity: 0.1
      });
      circle._pielh = { type: 'districts', item: d };
      circle.on('click', () => { _fireSelect('districts', d); });

      const label = L.marker([lat, lon], {
        icon: L.divIcon({
          className: 'map-label dist-label',
          html: d.name, iconAnchor: [-4, 36]
        }),
        interactive: false
      });
      circle.addTo(_layers.districts);
      label.addTo(_layers.districts);
    });
    _showOnly('districts');
  }

  // ── Public API ────────────────────────────────────────────────
  function highlightById(type, id) {
    const layer = _layers[type];
    if (!layer) return;
    layer.eachLayer(m => {
      if (!m._pielh) return;
      const sel = String(m._pielh.item.id) === String(id);
      if (m._icon) m._icon.classList.toggle('marker-selected', sel);
      if (sel) _selectedMarker = m;
    });
  }

  function zoomToSelected() {
    if (_selectedMarker && _selectedMarker.getLatLng) {
      _map.setView(_selectedMarker.getLatLng(), Math.max(_map.getZoom(), 17));
    }
  }

  function refresh() {
    setTimeout(() => _map && _map.invalidateSize(), 150);
  }

  return {
    init, onSelect,
    renderBuildings, renderSensors, renderNeighborhoods, renderDistricts,
    highlightById, zoomToSelected, refresh
  };
})();
