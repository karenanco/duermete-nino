/**
 * Mitos y Leyendas Mundiales - Interactive 3D Globe
 * Uses Globe.GL (Three.js based) for a beautiful interactive globe
 */

// =====================================================
// STATE
// =====================================================
let globeInstance = null;
let paisesData = {};  // { codigo_iso: { nombre, continente, seres_count } }
let activeCountryCode = null;

// =====================================================
// ISO CODE MAPPING (GeoJSON ISO_A2 → our DB codes)
// =====================================================
const ISO_MAP = {
  'GB': 'ENG',   // United Kingdom → England (our DB has England separate)
  // Add more mappings if needed
};

// Reverse map: our DB codes → GeoJSON ISO_A2
const REVERSE_ISO_MAP = {};
for (const [geo, db] of Object.entries(ISO_MAP)) {
  REVERSE_ISO_MAP[db] = geo;
}

function geoToDbCode(isoA2) {
  return ISO_MAP[isoA2] || isoA2;
}

function dbToGeoCode(dbCode) {
  return REVERSE_ISO_MAP[dbCode] || dbCode;
}

// =====================================================
// ARCHETYPE COLOR SCHEME
// =====================================================
const ARCHETYPE_COLORS = {
  1: { border: 'border-red-900/30', hover: 'hover:border-red-500/40', badge: 'bg-red-950 text-red-400 border-red-900', title: 'text-red-300', bg: 'from-red-900/10 to-transparent' },
  2: { border: 'border-amber-900/30', hover: 'hover:border-amber-500/40', badge: 'bg-amber-950 text-amber-400 border-amber-900', title: 'text-amber-300', bg: 'from-amber-900/10 to-transparent' },
  3: { border: 'border-cyan-900/30', hover: 'hover:border-cyan-500/40', badge: 'bg-cyan-950 text-cyan-400 border-cyan-900', title: 'text-cyan-300', bg: 'from-cyan-900/10 to-transparent' },
  4: { border: 'border-purple-900/30', hover: 'hover:border-purple-500/40', badge: 'bg-purple-950 text-purple-400 border-purple-900', title: 'text-purple-300', bg: 'from-purple-900/10 to-transparent' },
  5: { border: 'border-indigo-900/30', hover: 'hover:border-indigo-500/40', badge: 'bg-indigo-950 text-indigo-400 border-indigo-900', title: 'text-indigo-300', bg: 'from-indigo-900/10 to-transparent' },
};

function getArchetypeId(name) {
  const map = {
    'La devoradora de niños': 1, 'Devoradora': 1,
    'El secuestrador / Castigador': 2, 'Secuestrador': 2, 'Castigador': 2,
    'El espíritu acuático que atrae niños': 3, 'Espíritu acuático': 3, 'Acuático': 3,
    'El niño fantasma o espíritu infantil': 4, 'Niño fantasma': 4, 'Espíritu infantil': 4,
    'El protector del hogar': 5, 'Protector': 5, 'Protector del hogar': 5,
  };
  return map[name] || 5;
}

// =====================================================
// API CLIENT
// =====================================================
async function fetchJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

async function fetchPaises() {
  return fetchJSON('/api/paises/');
}

async function fetchSeresPorPais(codigoIso) {
  return fetchJSON(`/api/pais/${codigoIso}/seres/`);
}

// =====================================================
// UI HELPERS
// =====================================================
function showPlaceholder() {
  document.getElementById('placeholder-text').classList.remove('hidden');
  document.getElementById('content-display').classList.add('hidden');
}

function showContent() {
  document.getElementById('placeholder-text').classList.add('hidden');
  document.getElementById('content-display').classList.remove('hidden');
}

function showLoading() {
  document.getElementById('loading-state').classList.remove('hidden');
  document.getElementById('lista-criaturas').innerHTML = '';
  document.getElementById('empty-state').classList.add('hidden');
}

function hideLoading() {
  document.getElementById('loading-state').classList.add('hidden');
}

function renderCreatureCard(c) {
  const archId = getArchetypeId(c.arquetipo);
  const col = ARCHETYPE_COLORS[archId] || ARCHETYPE_COLORS[5];

  return `
    <div class="creature-card p-4 rounded-xl bg-gradient-to-b ${col.bg} bg-gray-950/80 border ${col.border} ${col.hover} cursor-pointer" data-ser-id="${c.id}">
      <div class="flex items-start justify-between gap-3">
        <h3 class="font-bold ${col.title} text-base">${c.nombre}</h3>
        <span class="shrink-0 px-2 py-0.5 ${col.badge} border text-[10px] font-semibold rounded-full uppercase tracking-wider whitespace-nowrap">${c.arquetipo.split('/')[0].trim()}</span>
      </div>
      <p class="text-sm text-gray-400 mt-2 leading-relaxed">${c.descripcion_breve}</p>
      <div class="mt-3 pt-3 border-t border-gray-800/30 hidden ser-detalle">
        <p class="text-xs text-gray-500 leading-relaxed">${c.descripcion_detallada || ''}</p>
      </div>
    </div>
  `;
}

function updateSidebar(data) {
  showContent();
  document.getElementById('txt-continente').textContent = data.continente || '';
  document.getElementById('txt-count').textContent = `${data.seres.length} ser${data.seres.length !== 1 ? 'es' : ''}`;
  document.getElementById('txt-pais').textContent = data.pais || '';

  const container = document.getElementById('lista-criaturas');
  container.innerHTML = '';

  if (data.seres && data.seres.length > 0) {
    data.seres.forEach((c, i) => {
      const html = renderCreatureCard(c);
      container.insertAdjacentHTML('beforeend', html);
    });

    // Click to toggle detail
    container.querySelectorAll('.creature-card').forEach(card => {
      card.addEventListener('click', () => {
        const detail = card.querySelector('.ser-detalle');
        if (detail) detail.classList.toggle('hidden');
      });
    });
  } else {
    document.getElementById('empty-state').classList.remove('hidden');
  }
}

function showCountryLabel(text) {
  const el = document.getElementById('country-label');
  document.getElementById('country-label-text').textContent = text;
  el.classList.remove('hidden');
}

function hideCountryLabel() {
  document.getElementById('country-label').classList.add('hidden');
}

// =====================================================
// GLOBE SETUP
// =====================================================
async function initGlobe() {
  const globeContainer = document.getElementById('globeViz');
  if (!globeContainer) return;

  // Fetch our country data
  try {
    const paisesResp = await fetchPaises();
    paisesData = {};
    for (const p of paisesResp.paises) {
      paisesData[p.codigo_iso] = p;
    }
  } catch (e) {
    console.warn('Could not fetch country data:', e);
  }

  // Fetch GeoJSON country boundaries
  const geoJsonUrl = 'https://cdn.jsdelivr.net/npm/three-globe/example/datasets/ne_110m_admin_0_countries.geojson';

  try {
    const geoResp = await fetch(geoJsonUrl);
    const countries = await geoResp.json();

    // Filter out Antarctica
    const features = countries.features.filter(d => d.properties.ISO_A2 !== 'AQ');

    // Enrich features with our data
    for (const feat of features) {
      const isoA2 = feat.properties.ISO_A2;
      const dbCode = geoToDbCode(isoA2);
      const ourData = paisesData[dbCode];
      feat.properties._dbCode = dbCode;
      feat.properties._hasData = !!ourData;
      feat.properties._seresCount = ourData ? ourData.seres_count : 0;
      feat.properties._nombrePais = ourData ? ourData.nombre : feat.properties.ADMIN;
      feat.properties._continente = ourData ? ourData.continente : '';
    }

    // Get the container dimensions
    const container = globeContainer.parentElement;
    const width = container.clientWidth;
    const height = container.clientHeight;

    // Color scale for countries with data
    const hasDataColor = '#818cf8';    // indigo-400
    const noDataColor = '#1e293b';     // slate-800
    const hoverColor = '#a5b4fc';      // indigo-300
    const activeColor = '#6366f1';     // indigo-500

    // Create globe
    const globe = Globe()
      .globeImageUrl('//cdn.jsdelivr.net/npm/three-globe/example/img/earth-dark.jpg')
      .backgroundImageUrl('//cdn.jsdelivr.net/npm/three-globe/example/img/night-sky.png')
      .width(width)
      .height(height)
      .polygonsData(features)
      .polygonAltitude(0.01)
      .polygonCapColor(feat => {
        if (feat.properties._isHovered) return hoverColor;
        if (feat.properties._isActive) return activeColor;
        return feat.properties._hasData ? hasDataColor : noDataColor;
      })
      .polygonSideColor(() => 'rgba(30, 41, 59, 0.3)')
      .polygonStrokeColor(() => 'rgba(15, 23, 42, 0.6)')
      .polygonLabel(feat => {
        const p = feat.properties;
        if (!p._hasData) return `<div style="color:#94a3b8;font-size:13px;font-family:sans-serif;"><b>${p.ADMIN}</b><br/><span style="color:#64748b;">Sin datos</span></div>`;
        return `<div style="color:#e2e8f0;font-size:13px;font-family:sans-serif;">
          <b style="color:#a5b4fc;">${p._nombrePais}</b><br/>
          <span style="color:#94a3b8;">${p._continente}</span><br/>
          <span style="color:#818cf8;">${p._seresCount} ser${p._seresCount !== 1 ? 'es' : ''}</span>
        </div>`;
      })
      .polygonLabel(d => '') // We handle labels via tooltip div instead
      .onPolygonHover((feat, prevFeat) => {
        // Reset previous
        if (prevFeat) {
          prevFeat.properties._isHovered = false;
        }
        // Set new
        if (feat) {
          feat.properties._isHovered = true;
          const p = feat.properties;
          if (p._hasData) {
            showCountryLabel(`${p._nombrePais} · ${p._seresCount} ser${p._seresCount !== 1 ? 'es' : ''}`);
          } else {
            showCountryLabel(p.ADMIN);
          }
        } else {
          hideCountryLabel();
        }
        // Refresh polygons
        globe.polygonsData(features);
      })
      .onPolygonClick(feat => {
        const p = feat.properties;
        if (!p._hasData) return;

        // Update active state
        features.forEach(f => { f.properties._isActive = false; });
        feat.properties._isActive = true;
        globe.polygonsData(features);

        // Load country data
        activeCountryCode = p._dbCode;
        showLoading();
        
        fetchSeresPorPais(p._dbCode)
          .then(data => {
            hideLoading();
            updateSidebar(data);
          })
          .catch(err => {
            console.error('Error loading country data:', err);
            hideLoading();
            document.getElementById('lista-criaturas').innerHTML = 
              '<p class="text-red-400 text-sm text-center py-8">Error al cargar datos.</p>';
          });
      })
      .polygonsTransitionDuration(200);

    globe(globeContainer);

    // Handle resize
    const resizeObserver = new ResizeObserver(entries => {
      for (const entry of entries) {
        const { width, height } = entry.contentRect;
        globe.width(width).height(height);
      }
    });
    resizeObserver.observe(container);

    // Hide loading overlay
    setTimeout(() => {
      const loading = document.getElementById('globe-loading');
      if (loading) {
        loading.style.opacity = '0';
        setTimeout(() => loading.classList.add('hidden'), 700);
      }
    }, 500);

    globeInstance = globe;

  } catch (err) {
    console.error('Failed to load globe:', err);
    const loading = document.getElementById('globe-loading');
    if (loading) {
      loading.innerHTML = `
        <div class="text-center">
          <p class="text-red-400 text-sm mb-2">Error al cargar el mapa</p>
          <button onclick="location.reload()" class="text-xs text-indigo-400 hover:text-indigo-300 underline">Reintentar</button>
        </div>
      `;
    }
  }
}

// =====================================================
// INITIALIZATION
// =====================================================
document.addEventListener('DOMContentLoaded', () => {
  showPlaceholder();
  initGlobe();
});

// Handle window resize
window.addEventListener('resize', () => {
  if (globeInstance) {
    const container = document.getElementById('globeViz').parentElement;
    globeInstance.width(container.clientWidth).height(container.clientHeight);
  }
});
