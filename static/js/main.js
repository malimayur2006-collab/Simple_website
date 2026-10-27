// Global main.js: Toasts, Search Modal, Navigation

function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  const bgColors = {
    success: 'bg-emerald-900/90 border-emerald-500 text-emerald-100',
    error: 'bg-rose-900/90 border-rose-500 text-rose-100',
    info: 'bg-sky-900/90 border-sky-500 text-sky-100',
    warning: 'bg-amber-900/90 border-amber-500 text-amber-100'
  };

  const icons = {
    success: '<i class="fa-solid fa-circle-check text-emerald-400 text-lg mr-3"></i>',
    error: '<i class="fa-solid fa-triangle-exclamation text-rose-400 text-lg mr-3"></i>',
    info: '<i class="fa-solid fa-circle-info text-sky-400 text-lg mr-3"></i>',
    warning: '<i class="fa-solid fa-circle-exclamation text-amber-400 text-lg mr-3"></i>'
  };

  toast.className = `flex items-center p-4 rounded-xl border shadow-2xl backdrop-blur-md toast-slide ${bgColors[type] || bgColors.info} max-w-md w-full mb-3`;
  toast.innerHTML = `
    ${icons[type] || icons.info}
    <div class="flex-1 text-sm font-medium leading-relaxed">${message}</div>
    <button onclick="this.parentElement.remove()" class="text-slate-400 hover:text-white ml-3 transition">
      <i class="fa-solid fa-xmark"></i>
    </button>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 4500);
}

// Global search setup
document.addEventListener('DOMContentLoaded', () => {
  const searchBtn = document.getElementById('nav-search-btn');
  const searchModal = document.getElementById('search-modal');
  const searchClose = document.getElementById('search-modal-close');
  const searchInput = document.getElementById('global-search-input');
  const searchResults = document.getElementById('search-results-list');

  function openSearch() {
    if (searchModal) {
      searchModal.classList.remove('hidden');
      if (searchInput) {
        searchInput.value = '';
        setTimeout(() => searchInput.focus(), 50);
      }
      if (searchResults) {
        searchResults.innerHTML = '<div class="text-center text-slate-400 py-6 text-sm">Type at least 2 characters to search across Jobs, Companies, Prep & DSA...</div>';
      }
    }
  }

  function closeSearch() {
    if (searchModal) {
      searchModal.classList.add('hidden');
    }
  }

  if (searchBtn) searchBtn.addEventListener('click', openSearch);
  if (searchClose) searchClose.addEventListener('click', closeSearch);

  // Keyboard shortcut Ctrl+K or Cmd+K
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      openSearch();
    }
    if (e.key === 'Escape' && searchModal && !searchModal.classList.contains('hidden')) {
      closeSearch();
    }
  });

  // Search input typing with debounce
  let searchTimeout = null;
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      clearTimeout(searchTimeout);
      const query = e.target.value.trim();
      if (query.length < 2) {
        searchResults.innerHTML = '<div class="text-center text-slate-400 py-6 text-sm">Type at least 2 characters to search...</div>';
        return;
      }

      searchResults.innerHTML = '<div class="text-center text-slate-400 py-6 text-sm"><i class="fa-solid fa-spinner fa-spin mr-2"></i>Searching portal...</div>';

      searchTimeout = setTimeout(async () => {
        try {
          const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
          const data = await res.json();
          if (data.results && data.results.length > 0) {
            searchResults.innerHTML = data.results.map(item => `
              <a href="${item.url}" class="flex items-center justify-between p-3 rounded-lg hover:bg-slate-700/60 border border-transparent hover:border-slate-600 transition group">
                <div class="flex items-center space-x-3">
                  <span class="px-2 py-0.5 text-xs rounded font-medium ${
                    item.type === 'Job' ? 'bg-indigo-500/20 text-indigo-300' :
                    item.type === 'Company' ? 'bg-amber-500/20 text-amber-300' :
                    item.type === 'Preparation' ? 'bg-emerald-500/20 text-emerald-300' :
                    'bg-cyan-500/20 text-cyan-300'
                  }">${item.type}</span>
                  <span class="text-slate-200 group-hover:text-white font-medium text-sm">${item.title}</span>
                </div>
                <span class="text-xs text-slate-400 font-mono">${item.badge || ''}</span>
              </a>
            `).join('');
          } else {
            searchResults.innerHTML = '<div class="text-center text-slate-400 py-6 text-sm">No results found for "' + query + '". Try a different keyword.</div>';
          }
        } catch (err) {
          searchResults.innerHTML = '<div class="text-center text-rose-400 py-6 text-sm">Error searching. Please try again.</div>';
        }
      }, 300);
    });
  }

  // Mobile navigation drawer toggle
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', () => {
      mobileMenu.classList.toggle('hidden');
    });
  }
});
