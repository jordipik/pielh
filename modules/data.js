// data.js — carga e indexa pielh_qa_master.json
const Data = (() => {
  let _raw = null;

  const SYSTEM_COLORS = [
    '#e74c3c','#3498db','#2ecc71','#f39c12','#9b59b6','#1abc9c',
    '#e67e22','#34495e','#e91e63','#00bcd4','#8bc34a','#ff5722',
    '#607d8b','#673ab7','#ffc107','#03a9f4','#4caf50','#ff9800',
    '#9c27b0','#795548','#f44336','#2196f3','#009688','#ffeb3b',
    '#3f51b5','#cddc39','#ff4081','#00e5ff'
  ];

  const _buildingById = {};
  const _sensorsByBuilding = {};
  const _systemColorMap = {};

  async function load(url) {
    const res = await fetch(url);
    _raw = await res.json();
    _buildIndexes();
    return _raw;
  }

  function _buildIndexes() {
    for (const b of _raw.buildings) {
      _buildingById[b.id] = b;
      _sensorsByBuilding[b.id] = [];
    }
    for (const s of _raw.sensors) {
      if (_sensorsByBuilding[s.hos]) _sensorsByBuilding[s.hos].push(s);
    }
    (_raw.catalogs.systems || []).forEach((sys, i) => {
      _systemColorMap[sys.id] = SYSTEM_COLORS[i % SYSTEM_COLORS.length];
    });
  }

  function getSystemColor(sysId) { return _systemColorMap[sysId] || '#94a3b8'; }
  function getBuilding(id) { return _buildingById[id]; }
  function getSensorsForBuilding(hos) { return _sensorsByBuilding[hos] || []; }

  function getAll(type) {
    if (!_raw) return [];
    switch (type) {
      case 'buildings':      return _raw.buildings;
      case 'sensors':        return _raw.sensors;
      case 'neighborhoods':  return _raw.catalogs.neighborhoods;
      case 'districts':      return _raw.catalogs.districts;
      case 'other_objects':  return _raw.other_objects;
      default: return [];
    }
  }

  function getSystems()       { return _raw ? _raw.catalogs.systems      : []; }
  function getNeighborhoods() { return _raw ? _raw.catalogs.neighborhoods : []; }
  function getDistricts()     { return _raw ? _raw.catalogs.districts     : []; }
  function getSummary()       { return _raw ? _raw.summary                : {}; }
  function getFindings()      { return _raw && _raw.qa ? _raw.qa.findings : []; }

  return {
    load, getAll, getBuilding, getSensorsForBuilding,
    getSystemColor, getSystems, getNeighborhoods, getDistricts,
    getSummary, getFindings
  };
})();
