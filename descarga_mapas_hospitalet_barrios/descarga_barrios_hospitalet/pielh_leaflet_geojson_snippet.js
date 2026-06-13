// ============================================================
// Integración Leaflet para límites de L'Hospitalet
// ============================================================

async function loadGeoJsonLayer(
    url,
    layerGroup,
    style,
    labelFieldCandidates = []
) {
    try {
        const res = await fetch(url);

        if (!res.ok) {
            throw new Error(`HTTP ${res.status}`);
        }

        const geojson = await res.json();

        const layer = L.geoJSON(geojson, {
            style,

            onEachFeature: (feature, leafletLayer) => {

                const props = feature.properties || {};

                const label =
                    labelFieldCandidates
                        .map(k => props[k])
                        .find(Boolean) ||
                    props.NOM ||
                    props.NOMBRE ||
                    props.name ||
                    props.id ||
                    'Sin nombre';

                leafletLayer.bindTooltip(
                    String(label),
                    {
                        permanent: false,
                        direction: 'center',
                        className: 'boundary-label'
                    }
                );

                leafletLayer.bindPopup(`
                    <div class="popup-title">${label}</div>
                `);
            }
        });

        layerGroup.addLayer(layer);

        return layer;

    } catch (err) {

        console.warn(
            `No se pudo cargar ${url}`,
            err
        );

        return null;
    }
}