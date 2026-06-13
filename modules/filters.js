// filters.js — estado de filtros y lógica de filtrado
const Filters = (() => {
  let _state = {
    type: 'buildings',
    system: '',
    neighborhood: '',
    district: '',
    text: ''
  };

  const _listeners = [];

  function onChanged(fn) { _listeners.push(fn); }
  function _notify()     { _listeners.forEach(fn => fn({ ..._state })); }

  function set(key, value) {
    _state[key] = value;
    _notify();
  }

  function getState() { return { ..._state }; }

  function apply(items, type) {
    let result = items;
    const { system, neighborhood, district, text } = _state;

    if (system && (type === 'sensors')) {
      result = result.filter(r => r.system_id === system);
    }
    if (neighborhood) {
      result = result.filter(r =>
        (r.neighborhood_key || r.neighborhood || r.key || '') === neighborhood
      );
    }
    if (district) {
      result = result.filter(r => r.district_code === district);
    }
    if (text) {
      const t = text.toLowerCase();
      result = result.filter(r => JSON.stringify(r).toLowerCase().includes(t));
    }
    return result;
  }

  return { onChanged, set, getState, apply };
})();
