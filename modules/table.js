// table.js — instancia Tabulator
const TableView = (() => {
  let _table = null;
  let _currentType = 'buildings';
  let _onSelect = null;
  let _built = false;
  let _pending = null;

  const COLS = {
    buildings: [
      { title: 'ID',       field: 'id',           width: 90,  frozen: true },
      { title: 'Nombre',   field: 'name',          minWidth: 200 },
      { title: 'Tipo',     field: 'type',          width: 120 },
      { title: 'Barrio',   field: 'neighborhood',  width: 120 },
      { title: 'Distrito', field: 'district_code', width: 100 },
      { title: 'Calle',    field: 'street_etra',   minWidth: 150 },
      { title: 'Estado',   field: 'state',         minWidth: 160 },
      { title: 'Datos',    field: 'has_data',      width: 95 },
      { title: '#Sens',    field: 'sensor_count',  width: 65, hozAlign: 'right' }
    ],
    sensors: [
      { title: 'ID',      field: 'id',          width: 170, frozen: true },
      { title: 'HOS',     field: 'hos',         width: 75 },
      { title: 'Sist.',   field: 'system_id',   width: 65,
        formatter: cell => {
          const v = cell.getValue();
          return `<span class="sys-badge" style="background:${Data.getSystemColor(v)}">${v}</span>`;
        }
      },
      { title: 'Sistema',   field: 'system_name',   minWidth: 180 },
      { title: 'Edificio',  field: 'building_name', minWidth: 190 },
      { title: 'Barrio',    field: 'neighborhood',  width: 110 },
      { title: 'REF-ETRA',  field: 'ref_etra',      width: 150 },
      { title: 'Datos',     field: 'has_data',      width: 90 },
      { title: 'Estado',    field: 'status',        width: 90 }
    ],
    neighborhoods: [
      { title: 'ID',        field: 'id',             width: 50 },
      { title: 'Nombre',    field: 'name',           minWidth: 150 },
      { title: 'Clave',     field: 'key',            width: 130 },
      { title: 'Distrito',  field: 'district_name',  width: 150 },
      { title: 'Edificios', field: 'building_count', width: 80, hozAlign: 'right' },
      { title: 'Sensores',  field: 'sensor_count',   width: 80, hozAlign: 'right' }
    ],
    districts: [
      { title: 'ID',        field: 'id',             width: 50 },
      { title: 'Código',    field: 'code',           width: 110 },
      { title: 'Nombre',    field: 'name',           width: 120 },
      { title: 'Descripción', field: 'description',  minWidth: 250 },
      { title: 'Edificios', field: 'building_count', width: 80, hozAlign: 'right' },
      { title: 'Sensores',  field: 'sensor_count',   width: 80, hozAlign: 'right' }
    ]
  };

  function init(containerId) {
    _table = new Tabulator('#' + containerId, {
      height: '100%',
      layout: 'fitDataFill',
      pagination: 'local',
      paginationSize: 50,
      paginationSizeSelector: [25, 50, 100, 200],
      movableColumns: true,
      selectable: 1,
      columns: COLS.buildings,
      rowClick(e, row) {
        if (_onSelect) _onSelect(_currentType, row.getData());
      },
      tableBuilt() {
        _built = true;
        if (_pending) { _doSetData(_pending.type, _pending.data); _pending = null; }
      }
    });
  }

  function onSelect(fn) { _onSelect = fn; }

  function _doSetData(type, data) {
    _currentType = type;
    _table.setColumns(COLS[type] || COLS.buildings);
    _table.setData(data);
  }

  function setData(type, data) {
    if (!_built) { _pending = { type, data }; return; }
    _doSetData(type, data);
  }

  function highlightRow(id) {
    _table.deselectRow();
    const rows = _table.getRows();
    for (const row of rows) {
      if (String(row.getData().id) === String(id)) {
        row.select();
        row.scrollTo();
        break;
      }
    }
  }

  function download() {
    _table.download('csv', `pielh_${_currentType}_export.csv`);
  }

  return { init, onSelect, setData, highlightRow, download };
})();
