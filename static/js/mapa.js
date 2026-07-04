/**
 * Duérmete Niño - Interactive Map Script
 * Handles API calls, UI updates, and globe interaction
 *
 * This is the main JavaScript for the interactive globe.
 * It provides:
 *   - API client for Django endpoints
 *   - UI controller for sidebar updates
 *   - Country selector (stand-in until WebGL globe is implemented)
 *   - Creature card rendering with archetype-based styling
 */

// =====================================================
// CONFIGURATION
// =====================================================

/**
 * Color palette per archetype.
 * Each entry defines Tailwind classes for borders, badges, and titles.
 */
const ARCHETYPE_COLORS = {
  1: { border: 'border-red-900/30', hover: 'hover:border-red-500/40', badge: 'bg-red-950 text-red-400 border-red-900', title: 'text-red-300' },
  2: { border: 'border-amber-900/30', hover: 'hover:border-amber-500/40', badge: 'bg-amber-950 text-amber-400 border-amber-900', title: 'text-amber-300' },
  3: { border: 'border-cyan-900/30', hover: 'hover:border-cyan-500/40', badge: 'bg-cyan-950 text-cyan-400 border-cyan-900', title: 'text-cyan-300' },
  4: { border: 'border-purple-900/30', hover: 'hover:border-purple-500/40', badge: 'bg-purple-950 text-purple-400 border-purple-900', title: 'text-purple-300' },
  5: { border: 'border-indigo-900/30', hover: 'hover:border-indigo-500/40', badge: 'bg-indigo-950 text-indigo-400 border-indigo-900', title: 'text-indigo-300' },
};

// =====================================================
// COUNTRY DATA
// =====================================================

/**
 * Hardcoded list of countries for the initial implementation
 * (before the WebGL globe is built).
 *
 * @type {Array<{codigo: string, nombre: string, continente: string}>}
 */
const PAISES = [
  // Europa
  { codigo: 'IS', nombre: 'Islandia', continente: 'Europa' },
  { codigo: 'AT', nombre: 'Austria', continente: 'Europa' },
  { codigo: 'PL', nombre: 'Polonia', continente: 'Europa' },
  { codigo: 'CZ', nombre: 'Chequia', continente: 'Europa' },
  { codigo: 'ENG', nombre: 'Inglaterra', continente: 'Europa' },
  { codigo: 'SCT', nombre: 'Escocia', continente: 'Europa' },
  { codigo: 'ES', nombre: 'España', continente: 'Europa' },
  { codigo: 'IE', nombre: 'Irlanda', continente: 'Europa' },
  { codigo: 'RU', nombre: 'Rusia', continente: 'Europa' },
  { codigo: 'NO', nombre: 'Noruega', continente: 'Europa' },
  { codigo: 'DK', nombre: 'Dinamarca', continente: 'Europa' },
  { codigo: 'FR', nombre: 'Francia', continente: 'Europa' },
  { codigo: 'BRE', nombre: 'Bretaña', continente: 'Europa' },
  { codigo: 'DE', nombre: 'Alemania', continente: 'Europa' },
  { codigo: 'SE', nombre: 'Suecia', continente: 'Europa' },
  { codigo: 'FI', nombre: 'Finlandia', continente: 'Europa' },
  // América Latina
  { codigo: 'MX', nombre: 'México', continente: 'América Latina' },
  { codigo: 'AR', nombre: 'Argentina', continente: 'América Latina' },
  { codigo: 'CO', nombre: 'Colombia', continente: 'América Latina' },
  { codigo: 'PY', nombre: 'Paraguay', continente: 'América Latina' },
  { codigo: 'CL', nombre: 'Chile', continente: 'América Latina' },
  { codigo: 'PE', nombre: 'Perú', continente: 'América Latina' },
  { codigo: 'CU', nombre: 'Cuba', continente: 'América Latina' },
  { codigo: 'VE', nombre: 'Venezuela', continente: 'América Latina' },
  // Norteamérica
  { codigo: 'CA', nombre: 'Canadá', continente: 'Norteamérica' },
  { codigo: 'US', nombre: 'Estados Unidos', continente: 'Norteamérica' },
  { codigo: 'HI', nombre: 'Hawái', continente: 'Norteamérica' },
  { codigo: 'GL', nombre: 'Groenlandia', continente: 'Norteamérica' },
  // Asia
  { codigo: 'JP', nombre: 'Japón', continente: 'Asia' },
  { codigo: 'ID', nombre: 'Indonesia', continente: 'Asia' },
  { codigo: 'MY', nombre: 'Malasia', continente: 'Asia' },
  { codigo: 'TH', nombre: 'Tailandia', continente: 'Asia' },
  { codigo: 'IN', nombre: 'India', continente: 'Asia' },
  { codigo: 'AE', nombre: 'Emiratos Árabes', continente: 'Asia' },
  { codigo: 'CN', nombre: 'China', continente: 'Asia' },
  { codigo: 'PH', nombre: 'Filipinas', continente: 'Asia' },
  // África
  { codigo: 'ZA', nombre: 'Sudáfrica', continente: 'África' },
  { codigo: 'GH', nombre: 'Ghana', continente: 'África' },
  { codigo: 'NG', nombre: 'Nigeria', continente: 'África' },
  { codigo: 'BJ', nombre: 'Benín', continente: 'África' },
  { codigo: 'GM', nombre: 'Gambia', continente: 'África' },
  { codigo: 'KE', nombre: 'Kenia', continente: 'África' },
  // Oceanía
  { codigo: 'AU', nombre: 'Australia', continente: 'Oceanía' },
  { codigo: 'NZ', nombre: 'Nueva Zelanda', continente: 'Oceanía' },
  { codigo: 'SB', nombre: 'Islas Salomón', continente: 'Oceanía' },
  { codigo: 'PF', nombre: 'Polinesia', continente: 'Oceanía' },
  { codigo: 'PG', nombre: 'Papúa Nueva Guinea', continente: 'Oceanía' },
];

// =====================================================
// API CLIENT
// =====================================================

/**
 * Generic JSON fetcher with error handling.
 * @param {string} url
 * @returns {Promise<object>}
 */
async function fetchJSON(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }
  return response.json();
}

/**
 * GET /api/seres/ — Returns all beings.
 * @returns {Promise<Array>}
 */
async function fetchSeres() {
  return fetchJSON('/api/seres/');
}

/**
 * GET /api/pais/{codigo}/seres/ — Returns beings for a specific country.
 * @param {string} codigoIso — ISO 3166-1 alpha-2 country code
 * @returns {Promise<object>}
 */
async function fetchSeresPorPais(codigoIso) {
  return fetchJSON(`/api/pais/${codigoIso}/seres/`);
}

/**
 * GET /api/ser/{id}/ — Returns detailed info for a single creature.
 * @param {number|string} serId
 * @returns {Promise<object>}
 */
async function fetchDetalleSer(serId) {
  return fetchJSON(`/api/ser/${serId}/`);
}

// =====================================================
// UI CONTROLLER
// =====================================================

/**
 * Show the default placeholder message in the sidebar.
 */
function showPlaceholder() {
  const placeholder = document.getElementById('placeholder-text');
  const content = document.getElementById('content-display');
  if (placeholder) placeholder.classList.remove('hidden');
  if (content) content.classList.add('hidden');
}

/**
 * Show the country-info / creature-list content in the sidebar.
 */
function showContentDisplay() {
  const placeholder = document.getElementById('placeholder-text');
  const content = document.getElementById('content-display');
  if (placeholder) placeholder.classList.add('hidden');
  if (content) content.classList.remove('hidden');
}

/**
 * Create an HTML card for a single creature.
 * Card border color is determined by the creature's archetype:
 *   1 → red   (La devoradora de niños)
 *   2 → amber (El secuestrador / Castigador)
 *   3 → cyan  (El espíritu acuático que atrae niños)
 *   4 → purple(El niño fantasma o espíritu infantil)
 *   5 → indigo(El protector del hogar)
 *
 * @param {object} criatura — Creature object from the API
 * @returns {string} HTML string
 */
function renderCreatureCard(criatura) {
  const archId = getArchetypeId(criatura.arquetipo);
  const colors = ARCHETYPE_COLORS[archId] || ARCHETYPE_COLORS[5];

  return `
    <div class="p-4 rounded-xl bg-gray-950/60 border ${colors.border} ${colors.hover} transition-all duration-300 cursor-pointer" data-ser-id="${criatura.id}">
      <div class="flex justify-between items-start">
        <h3 class="font-bold text-lg ${colors.title}">${criatura.nombre}</h3>
        <span class="px-2 py-0.5 ${colors.badge} border text-[10px] font-semibold rounded-full uppercase">${criatura.arquetipo}</span>
      </div>
      <p class="text-sm text-gray-300 mt-1">${criatura.descripcion_breve || ''}</p>
    </div>
  `;
}

/**
 * Map an archetype name string to a numeric ID for color selection.
 * Accepts partial and full Spanish names.
 *
 * @param {string} nombreArquetipo
 * @returns {number} 1–5
 */
function getArchetypeId(nombreArquetipo) {
  const map = {
    'La devoradora de niños': 1,
    'Devoradora': 1,
    'El secuestrador / Castigador': 2,
    'Secuestrador': 2,
    'Castigador': 2,
    'El espíritu acuático que atrae niños': 3,
    'Espíritu acuático': 3,
    'El niño fantasma o espíritu infantil': 4,
    'Niño fantasma': 4,
    'Espíritu infantil': 4,
    'El protector del hogar': 5,
    'Protector': 5,
    'Protector del hogar': 5,
  };
  return map[nombreArquetipo] || 5;
}

/**
 * Update the sidebar with country info and a list of creatures.
 *
 * @param {object} data — Response shape: { pais, continente, seres: [...] }
 */
function updateSidebar(data) {
  showContentDisplay();

  const txtContinente = document.getElementById('txt-continente');
  const txtPais = document.getElementById('txt-pais');
  const container = document.getElementById('lista-criaturas');

  if (txtContinente) txtContinente.textContent = data.continente || '';
  if (txtPais) txtPais.textContent = data.pais || '';
  if (!container) return;

  container.innerHTML = '';

  if (data.seres && data.seres.length > 0) {
    data.seres.forEach(function (criatura) {
      container.insertAdjacentHTML('beforeend', renderCreatureCard(criatura));
    });
  } else {
    container.innerHTML =
      '<p class="text-gray-500 text-sm text-center py-8">No se encontraron seres folclóricos registrados para este país.</p>';
  }
}

/**
 * Show a loading spinner inside the creatures list container.
 */
function showLoading() {
  const container = document.getElementById('lista-criaturas');
  if (container) {
    container.innerHTML =
      '<div class="text-center py-8" role="status">' +
      '<div class="animate-spin h-8 w-8 border-2 border-indigo-500 border-t-transparent rounded-full mx-auto"></div>' +
      '<p class="text-gray-500 text-sm mt-2">Cargando...</p>' +
      '</div>';
  }
}

// =====================================================
// COUNTRY SELECTOR UI
// =====================================================

/**
 * Build the country-selector button (positioned inside the globe container)
 * and the modal with search + continent filters.
 */
function createCountrySelector() {
  var globeContainer = document.getElementById('globe-container');
  if (!globeContainer) return;

  /* ---------- Trigger button ---------- */
  var btn = document.createElement('button');
  btn.id = 'btn-selector-paises';
  btn.className =
    'absolute top-4 right-4 bg-gray-950/80 border border-gray-800 px-3 py-2 rounded-xl text-xs text-indigo-300 hover:bg-gray-800 transition z-20 flex items-center gap-2';
  btn.setAttribute('aria-label', 'Abrir selector de países');
  btn.innerHTML =
    '<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg> Explorar países';
  globeContainer.appendChild(btn);

  /* ---------- Modal ---------- */
  var modal = document.createElement('div');
  modal.id = 'selector-paises-modal';
  modal.className =
    'hidden fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm';
  modal.setAttribute('role', 'dialog');
  modal.setAttribute('aria-modal', 'true');
  modal.setAttribute('aria-label', 'Seleccionar país');
  modal.innerHTML =
    '<div class="bg-gray-900 border border-gray-800 rounded-2xl w-full max-w-lg max-h-[80vh] flex flex-col shadow-2xl">' +
    '  <div class="flex items-center justify-between p-4 border-b border-gray-800">' +
    '    <h3 class="text-lg font-bold text-indigo-300">Seleccionar País</h3>' +
    '    <button id="btn-cerrar-selector" class="text-gray-500 hover:text-gray-300 transition" aria-label="Cerrar selector">' +
    '      <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>' +
    '    </button>' +
    '  </div>' +
    '  <div class="p-4 border-b border-gray-800">' +
    '    <input id="buscador-paises" type="text" placeholder="Buscar país…" class="w-full bg-gray-950 border border-gray-800 rounded-lg px-4 py-2 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-indigo-500 transition">' +
    '  </div>' +
    '  <div class="flex gap-1 p-2 border-b border-gray-800 overflow-x-auto" role="tablist" aria-label="Filtrar por continente">' +
    '    <button data-continente="todos" class="btn-filtro-continente px-3 py-1 rounded-full text-xs bg-indigo-900/50 text-indigo-300 border border-indigo-800 whitespace-nowrap" role="tab" aria-selected="true">Todos</button>' +
    '    <button data-continente="Europa" class="btn-filtro-continente px-3 py-1 rounded-full text-xs bg-gray-800 text-gray-400 hover:bg-gray-700 whitespace-nowrap" role="tab">Europa</button>' +
    '    <button data-continente="América Latina" class="btn-filtro-continente px-3 py-1 rounded-full text-xs bg-gray-800 text-gray-400 hover:bg-gray-700 whitespace-nowrap" role="tab">América Latina</button>' +
    '    <button data-continente="Norteamérica" class="btn-filtro-continente px-3 py-1 rounded-full text-xs bg-gray-800 text-gray-400 hover:bg-gray-700 whitespace-nowrap" role="tab">Norteamérica</button>' +
    '    <button data-continente="Asia" class="btn-filtro-continente px-3 py-1 rounded-full text-xs bg-gray-800 text-gray-400 hover:bg-gray-700 whitespace-nowrap" role="tab">Asia</button>' +
    '    <button data-continente="África" class="btn-filtro-continente px-3 py-1 rounded-full text-xs bg-gray-800 text-gray-400 hover:bg-gray-700 whitespace-nowrap" role="tab">África</button>' +
    '    <button data-continente="Oceanía" class="btn-filtro-continente px-3 py-1 rounded-full text-xs bg-gray-800 text-gray-400 hover:bg-gray-700 whitespace-nowrap" role="tab">Oceanía</button>' +
    '  </div>' +
    '  <div id="lista-paises" class="overflow-y-auto p-2 flex-1" role="listbox">' +
        renderPaisList(PAISES) +
    '  </div>' +
    '</div>';
  document.body.appendChild(modal);

  /* ---------- Event listeners ---------- */
  document.getElementById('btn-selector-paises').addEventListener('click', function () {
    modal.classList.remove('hidden');
    // Focus the search input when the modal opens
    setTimeout(function () {
      document.getElementById('buscador-paises').focus();
    }, 100);
  });

  document.getElementById('btn-cerrar-selector').addEventListener('click', function () {
    modal.classList.add('hidden');
  });

  modal.addEventListener('click', function (e) {
    if (e.target === modal) modal.classList.add('hidden');
  });

  // Close on Escape
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !modal.classList.contains('hidden')) {
      modal.classList.add('hidden');
    }
  });

  // Search input
  document.getElementById('buscador-paises').addEventListener('input', function (e) {
    filterCountries(e.target.value);
  });

  // Continent filter buttons
  document.querySelectorAll('.btn-filtro-continente').forEach(function (btn) {
    btn.addEventListener('click', function () {
      // De-select all, select this one
      document.querySelectorAll('.btn-filtro-continente').forEach(function (b) {
        b.classList.remove('bg-indigo-900/50', 'text-indigo-300', 'border-indigo-800');
        b.classList.add('bg-gray-800', 'text-gray-400');
        b.setAttribute('aria-selected', 'false');
      });
      btn.classList.remove('bg-gray-800', 'text-gray-400');
      btn.classList.add('bg-indigo-900/50', 'text-indigo-300', 'border-indigo-800');
      btn.setAttribute('aria-selected', 'true');
      filterCountries(document.getElementById('buscador-paises').value);
    });
  });
}

/**
 * Render the list of countries, grouped by continent.
 *
 * @param {Array} paises
 * @returns {string} HTML
 */
function renderPaisList(paises) {
  var continentes = {};
  paises.forEach(function (p) {
    if (!continentes[p.continente]) continentes[p.continente] = [];
    continentes[p.continente].push(p);
  });

  var html = '';
  var continenteKeys = Object.keys(continentes);
  for (var i = 0; i < continenteKeys.length; i++) {
    var continente = continenteKeys[i];
    var items = continentes[continente];
    html += '<div class="mb-3">';
    html +=
      '<h4 class="text-[10px] uppercase tracking-widest text-indigo-500 font-bold px-3 py-1">' +
      continente +
      '</h4>';
    for (var j = 0; j < items.length; j++) {
      var p = items[j];
      html +=
        '<button data-codigo="' +
        p.codigo +
        '" class="btn-pais w-full text-left px-4 py-2 rounded-lg hover:bg-gray-800 transition text-sm text-gray-300 hover:text-white flex items-center gap-3" role="option">' +
        '  <span class="w-2 h-2 rounded-full bg-indigo-600" aria-hidden="true"></span>' +
        p.nombre +
        '</button>';
    }
    html += '</div>';
  }
  return html;
}

/**
 * Filter the country list by search query and active continent tab,
 * then re-render.
 *
 * @param {string} query
 */
function filterCountries(query) {
  var q = query.toLowerCase().trim();
  var activeFiltro = document.querySelector(
    '.btn-filtro-continente.bg-indigo-900\\/50'
  );
  var continenteFiltro = activeFiltro ? activeFiltro.dataset.continente : 'todos';

  var filtered = PAISES;
  if (continenteFiltro !== 'todos') {
    filtered = filtered.filter(function (p) {
      return p.continente === continenteFiltro;
    });
  }
  if (q) {
    filtered = filtered.filter(function (p) {
      return p.nombre.toLowerCase().includes(q);
    });
  }

  var container = document.getElementById('lista-paises');
  if (!container) return;

  if (filtered.length > 0) {
    container.innerHTML = renderPaisList(filtered);
  } else {
    container.innerHTML =
      '<p class="text-gray-500 text-sm text-center py-8">No se encontraron países.</p>';
  }

  // Re-bind click events on new buttons
  container.querySelectorAll('.btn-pais').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var codigo = btn.dataset.codigo;
      var modal = document.getElementById('selector-paises-modal');
      if (modal) modal.classList.add('hidden');
      cargarPais(codigo);
    });
  });
}

// =====================================================
// MAIN INTERACTION
// =====================================================

/**
 * Load creatures for a given country and update the sidebar.
 *
 * @param {string} codigoIso — ISO 3166-1 alpha-2 code
 */
async function cargarPais(codigoIso) {
  showLoading();
  try {
    var data = await fetchSeresPorPais(codigoIso);
    updateSidebar(data);
  } catch (error) {
    console.error('Error al cargar país:', error);
    var container = document.getElementById('lista-criaturas');
    if (container) {
      container.innerHTML =
        '<p class="text-red-400 text-sm text-center py-8">Error al cargar los datos. Intenta de nuevo.</p>';
    }
  }
}

// =====================================================
// INITIALIZATION
// =====================================================

document.addEventListener('DOMContentLoaded', function () {
  createCountrySelector();
  showPlaceholder();
});
