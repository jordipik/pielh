// qa_explorer_app.js — inicialización y cableado de módulos
(async () => {
  const DATA_URL = 'pielh_qa_master.json';

  const loadingEl   = document.getElementById('loading-overlay');
  const loadingText = document.getElementById('loading-text');

  function setLoading(msg) { loadingText.textContent = msg; }
  function hideLoading()   { loadingEl.style.display = 'none'; }

  setLoading('Inicializando mapa…');
  MapView.init('map');

  setLoading('Cargando pielh_qa_master.json…');
  await Data.load(DATA_URL);

  _populateDropdowns();

  setLoading('Inicializando tabla…');
  const _initialData = Filters.apply(Data.getAll('buildings'), 'buildings');
  TableView.init('table-container', 'buildings', _initialData);

  TableView.onSelect((type, item) => {
    Details.render(type, item);
    MapView.highlightById(type, item.id);
  });

  MapView.onSelect((type, item) => {
    Details.render(type, item);
    TableView.highlightRow(item.id);
  });

  Filters.onChanged(state => _applyAll(state));

  document.querySelectorAll('.type-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.type-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      Filters.set('type', btn.dataset.type);
    });
  });

  document.getElementById('filter-system').addEventListener('change', e =>
    Filters.set('system', e.target.value));
  document.getElementById('filter-neighborhood').addEventListener('change', e =>
    Filters.set('neighborhood', e.target.value));
  document.getElementById('filter-district').addEventListener('change', e =>
    Filters.set('district', e.target.value));

  let _textTimer;
  document.getElementById('filter-text').addEventListener('input', e => {
    clearTimeout(_textTimer);
    _textTimer = setTimeout(() => Filters.set('text', e.target.value), 250);
  });

  document.getElementById('btn-export').addEventListener('click', () => TableView.download());
  document.getElementById('btn-zoom').addEventListener('click',   () => MapView.zoomToSelected());

  setLoading('Renderizando…');
  _updateAllCounters();
  _applyAll(Filters.getState());

  hideLoading();
  MapView.refresh();

  function _populateDropdowns() {
    const sysSel   = document.getElementById('filter-system');
    const neighSel = document.getElementById('filter-neighborhood');
    const distSel  = document.getElementById('filter-district');

    Data.getSystems().forEach(s => {
      sysSel.appendChild(new Option(`${s.id} — ${s.name}`, s.id));
    });
    Data.getNeighborhoods().forEach(n => {
      neighSel.appendChild(new Option(n.name, n.key));
    });
    Data.getDistricts().forEach(d => {
      distSel.appendChild(new Option(d.name, d.code));
    });
  }

  function _applyAll(state) {
    const { type } = state;
    const all      = Data.getAll(type);
    const filtered = Filters.apply(all, type);

    TableView.setData(type, filtered);

    switch (type) {
      case 'buildings':
        MapView.renderBuildings(filtered);
        break;
      case 'sensors':
        MapView.renderSensors(filtered, Data.getAll('buildings'));
        break;
      case 'neighborhoods':
        MapView.renderNeighborhoods(filtered);
        break;
      case 'districts':
        MapView.renderDistricts(filtered);
        break;
    }

    const cntEl = document.getElementById(`cnt-${type}`);
    if (cntEl) cntEl.textContent = filtered.length;

    Details.clear();
  }

  function _updateAllCounters() {
    ['buildings','sensors','neighborhoods','districts'].forEach(t => {
      const el = document.getElementById(`cnt-${t}`);
      if (el) el.textContent = Data.getAll(t).length;
    });
  }
})();
