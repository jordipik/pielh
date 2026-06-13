// details.js — panel inferior de ficha
const Details = (() => {
  const el = () => document.getElementById('detail-panel');

  function _row(label, value) {
    if (value === null || value === undefined || value === '') return '';
    return `<div class="dr"><span class="dl">${label}</span><span class="dv">${value}</span></div>`;
  }

  function renderBuilding(b) {
    const sensors = Data.getSensorsForBuilding(b.id);
    const sysIds = [...new Set(sensors.map(s => s.system_id))];

    el().innerHTML = `
      <div class="dh">
        <span class="dbadge bld">EDIFICIO</span>
        <span class="dtitle">${b.name}</span>
        <span class="dsubtitle">${b.id}</span>
      </div>
      <div class="dbody">
        <div class="dcols">
          <div>
            ${_row('Calle',     b.street_etra)}
            ${_row('Barrio',    b.neighborhood)}
            ${_row('Distrito',  b.district_name)}
            ${_row('Tipo',      b.type)}
            ${_row('Zona',      b.zone)}
          </div>
          <div>
            ${_row('Coords',    b.lat ? `${b.lat.toFixed(6)}, ${b.lon.toFixed(6)}` : null)}
            ${_row('Sensores',  b.sensor_count)}
            ${_row('Sistemas',  sysIds.length || null)}
            ${_row('Estado',    b.state)}
            ${_row('Datos',     b.has_data)}
          </div>
        </div>
        ${sysIds.length ? `<div class="dtags">${sysIds.map(sid =>
          `<span class="sys-badge" style="background:${Data.getSystemColor(sid)}" title="${sid}">${sid}</span>`
        ).join('')}</div>` : ''}
        ${sensors.length ? `
        <div class="dtable">
          <table>
            <thead><tr><th>ID Sensor</th><th>Sistema</th><th>REF-ETRA</th><th>Datos</th></tr></thead>
            <tbody>
              ${sensors.slice(0, 25).map(s => `
                <tr>
                  <td class="mono">${s.id}</td>
                  <td><span class="sys-badge" style="background:${Data.getSystemColor(s.system_id)}">${s.system_id}</span> ${s.system_name}</td>
                  <td class="mono">${s.ref_etra || '—'}</td>
                  <td>${s.has_data || '—'}</td>
                </tr>`).join('')}
              ${sensors.length > 25 ? `<tr><td colspan="4" class="more-row">… y ${sensors.length - 25} sensores más</td></tr>` : ''}
            </tbody>
          </table>
        </div>` : ''}
      </div>`;
  }

  function renderSensor(s) {
    el().innerHTML = `
      <div class="dh">
        <span class="dbadge sensor" style="background:${Data.getSystemColor(s.system_id)}">SENSOR</span>
        <span class="dtitle">${s.id}</span>
        <span class="dsubtitle">${s.system_name}</span>
      </div>
      <div class="dbody">
        <div class="dcols">
          <div>
            ${_row('Edificio',  s.building_name)}
            ${_row('HOS',       s.hos)}
            ${_row('Sistema',   `${s.system_id} · ${s.system_name}`)}
            ${_row('REF-ETRA',  s.ref_etra)}
          </div>
          <div>
            ${_row('Barrio',    s.neighborhood)}
            ${_row('Distrito',  s.district_name)}
            ${_row('Coords',    s.lat ? `${s.lat.toFixed(6)}, ${s.lon.toFixed(6)}` : null)}
            ${_row('Datos',     s.has_data)}
            ${_row('Estado',    s.status)}
            ${_row('Include',   s.include)}
          </div>
        </div>
      </div>`;
  }

  function renderNeighborhood(n) {
    el().innerHTML = `
      <div class="dh">
        <span class="dbadge neigh">BARRIO</span>
        <span class="dtitle">${n.name}</span>
        <span class="dsubtitle">${n.key}</span>
      </div>
      <div class="dbody">
        <div class="dcols">
          <div>
            ${_row('Distrito',  n.district_name)}
            ${_row('Edificios', n.building_count)}
            ${_row('Sensores',  n.sensor_count)}
          </div>
          <div>
            ${_row('Coords',    n.lat ? `${n.lat.toFixed(6)}, ${n.lon.toFixed(6)}` : null)}
            ${_row('Thing ID',  n.thing_id)}
          </div>
        </div>
      </div>`;
  }

  function renderDistrict(d) {
    el().innerHTML = `
      <div class="dh">
        <span class="dbadge dist">DISTRITO</span>
        <span class="dtitle">${d.name}</span>
        <span class="dsubtitle">${d.code}</span>
      </div>
      <div class="dbody">
        <div class="dcols">
          <div>
            ${_row('Descripción', d.description)}
            ${_row('Edificios',   d.building_count)}
            ${_row('Sensores',    d.sensor_count)}
          </div>
        </div>
      </div>`;
  }

  function render(type, item) {
    switch (type) {
      case 'buildings':     renderBuilding(item);     break;
      case 'sensors':       renderSensor(item);       break;
      case 'neighborhoods': renderNeighborhood(item); break;
      case 'districts':     renderDistrict(item);     break;
      default:
        el().innerHTML = `<pre class="detail-raw">${JSON.stringify(item, null, 2)}</pre>`;
    }
  }

  function clear() {
    el().innerHTML = '<div class="detail-empty">Selecciona un elemento para ver su ficha</div>';
  }

  return { render, clear };
})();
