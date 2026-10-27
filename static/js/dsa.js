// dsa.js: Topic-wise Sheet Tracker, Code Modal, Personal Notes, Filters

let dsaProblemsMap = {};
let activeNoteProblemId = null;

document.addEventListener('DOMContentLoaded', () => {
  const dataEl = document.getElementById('dsa-data');
  if (dataEl) {
    try {
      dsaProblemsMap = JSON.parse(dataEl.textContent);
    } catch (e) {
      console.error('Error parsing DSA problems JSON', e);
    }
  }
});

async function toggleProblemSolved(problemId, checkboxEl) {
  try {
    const res = await fetch('/api/dsa/toggle-solved', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ problem_id: problemId })
    });
    const data = await res.json();
    if (data.success) {
      // Update row appearance and dataset
      const rowEl = document.getElementById(`dsa-row-${problemId}`);
      if (rowEl) {
        rowEl.dataset.solved = data.is_solved ? 'true' : 'false';
        if (data.is_solved) {
          rowEl.classList.add('bg-emerald-950/20');
        } else {
          rowEl.classList.remove('bg-emerald-950/20');
        }
      }

      // Update in local map
      if (dsaProblemsMap[problemId]) {
        dsaProblemsMap[problemId].is_solved = data.is_solved;
      }

      // Update overall progress bar & counters
      const overallPercent = document.getElementById('overall-dsa-percent');
      const overallBar = document.getElementById('overall-dsa-bar');
      const overallSolved = document.getElementById('overall-dsa-solved');

      if (overallPercent) overallPercent.textContent = `${data.percent}%`;
      if (overallBar) overallBar.style.width = `${data.percent}%`;
      if (overallSolved) overallSolved.textContent = data.solved;

      showToast(data.is_solved ? 'Marked problem as solved! 🎯' : 'Marked problem as unsolved.');
    }
  } catch (err) {
    showToast('Failed to update problem status.', 'error');
    if (checkboxEl) checkboxEl.checked = !checkboxEl.checked;
  }
}

async function toggleProblemRevision(problemId, buttonEl) {
  try {
    const res = await fetch('/api/dsa/toggle-revision', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ problem_id: problemId })
    });
    const data = await res.json();
    if (data.success) {
      const rowEl = document.getElementById(`dsa-row-${problemId}`);
      if (rowEl) {
        rowEl.dataset.revision = data.is_revision ? 'true' : 'false';
      }

      if (dsaProblemsMap[problemId]) {
        dsaProblemsMap[problemId].is_revision = data.is_revision;
      }

      if (buttonEl) {
        if (data.is_revision) {
          buttonEl.innerHTML = '<i class="fa-solid fa-star text-amber-400"></i>';
          buttonEl.title = 'Marked for Revision';
        } else {
          buttonEl.innerHTML = '<i class="fa-regular fa-star text-slate-500 hover:text-amber-400"></i>';
          buttonEl.title = 'Add to Revision';
        }
      }
      showToast(data.is_revision ? 'Saved to Revision list! ⭐' : 'Removed from Revision list.');
    }
  } catch (err) {
    showToast('Failed to toggle revision status.', 'error');
  }
}

function openSolutionModal(problemId) {
  const p = dsaProblemsMap[problemId];
  if (!p) {
    showToast('Problem data not found.', 'error');
    return;
  }

  const modal = document.getElementById('dsa-solution-modal');
  if (!modal) return;

  document.getElementById('sol-modal-title').textContent = p.title;
  document.getElementById('sol-modal-topic').textContent = p.topic;
  
  const diffEl = document.getElementById('sol-modal-difficulty');
  diffEl.textContent = p.difficulty;
  diffEl.className = `px-2.5 py-0.5 rounded-full text-xs font-semibold ${
    p.difficulty === 'Easy' ? 'badge-easy' : p.difficulty === 'Medium' ? 'badge-medium' : 'badge-hard'
  }`;

  const lcLink = document.getElementById('sol-modal-leetcode');
  const gfgLink = document.getElementById('sol-modal-gfg');
  if (lcLink) {
    lcLink.href = p.leetcode_url || '#';
    lcLink.style.display = p.leetcode_url ? 'inline-flex' : 'none';
  }
  if (gfgLink) {
    gfgLink.href = p.gfg_url || '#';
    gfgLink.style.display = p.gfg_url ? 'inline-flex' : 'none';
  }

  document.getElementById('sol-modal-desc').textContent = p.description || 'Solve the problem following optimal constraints.';
  document.getElementById('sol-modal-approach').innerHTML = p.approach || 'Optimal approach using two pointers/hashmap.';
  document.getElementById('sol-modal-time').textContent = p.time_complexity || 'O(N)';
  document.getElementById('sol-modal-space').textContent = p.space_complexity || 'O(1)';

  // Code snippets
  window.currentProblemCodes = {
    python: p.code_python || '# Python solution coming soon',
    cpp: p.code_cpp || '// C++ solution coming soon',
    java: p.code_java || '// Java solution coming soon'
  };

  switchCodeTab('python');

  modal.classList.remove('hidden');
  document.body.style.overflow = 'hidden';
}

function switchCodeTab(lang) {
  const tabs = document.querySelectorAll('.code-tab-btn');
  tabs.forEach(btn => {
    if (btn.dataset.lang === lang) {
      btn.classList.add('bg-slate-700', 'text-white', 'border-indigo-500');
      btn.classList.remove('text-slate-400');
    } else {
      btn.classList.remove('bg-slate-700', 'text-white', 'border-indigo-500');
      btn.classList.add('text-slate-400');
    }
  });

  const codeEl = document.getElementById('sol-modal-code');
  if (codeEl && window.currentProblemCodes) {
    codeEl.textContent = window.currentProblemCodes[lang] || '';
  }
}

function copyCurrentCode() {
  const codeEl = document.getElementById('sol-modal-code');
  if (!codeEl) return;
  navigator.clipboard.writeText(codeEl.textContent).then(() => {
    showToast('Code copied to clipboard! 📋', 'success');
  }).catch(() => {
    showToast('Could not copy code.', 'error');
  });
}

function closeSolutionModal() {
  const modal = document.getElementById('dsa-solution-modal');
  if (modal) {
    modal.classList.add('hidden');
    document.body.style.overflow = 'auto';
  }
}

// Personal Notes Modal
function openNotesModal(problemId) {
  activeNoteProblemId = problemId;
  const p = dsaProblemsMap[problemId];

  const modal = document.getElementById('dsa-notes-modal');
  const titleEl = document.getElementById('notes-modal-title');
  const textarea = document.getElementById('notes-modal-textarea');

  if (titleEl) titleEl.textContent = p ? p.title : `Problem #${problemId}`;
  if (textarea) textarea.value = p ? (p.user_notes || '') : '';

  if (modal) {
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }
}

function closeNotesModal() {
  const modal = document.getElementById('dsa-notes-modal');
  if (modal) {
    modal.classList.add('hidden');
    document.body.style.overflow = 'auto';
  }
}

async function savePersonalNote() {
  if (!activeNoteProblemId) return;
  const textarea = document.getElementById('notes-modal-textarea');
  const note = textarea ? textarea.value.trim() : '';

  try {
    const res = await fetch('/api/dsa/save-note', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ problem_id: activeNoteProblemId, note: note })
    });
    const data = await res.json();
    if (data.success) {
      if (dsaProblemsMap[activeNoteProblemId]) {
        dsaProblemsMap[activeNoteProblemId].user_notes = note;
      }
      showToast('Personal notes saved!', 'success');
      closeNotesModal();
    } else {
      showToast('Could not save note.', 'error');
    }
  } catch (err) {
    showToast('Network error while saving note.', 'error');
  }
}

// Filtering problem rows in DSA sheet
function applyDSAFilters() {
  const searchInput = document.getElementById('dsa-search-input');
  const query = searchInput ? searchInput.value.toLowerCase().trim() : '';

  const diffFilter = document.getElementById('dsa-diff-filter');
  const selectedDiff = diffFilter ? diffFilter.value : 'all';

  const statusFilter = document.getElementById('dsa-status-filter');
  const selectedStatus = statusFilter ? statusFilter.value : 'all';

  const rows = document.querySelectorAll('.dsa-problem-row');

  rows.forEach(row => {
    const title = (row.dataset.title || '').toLowerCase();
    const diff = row.dataset.diff || '';
    const isSolved = row.dataset.solved === 'true';
    const isRev = row.dataset.revision === 'true';

    let matchQuery = query === '' || title.includes(query);
    let matchDiff = selectedDiff === 'all' || diff === selectedDiff;
    let matchStatus = true;
    if (selectedStatus === 'solved') matchStatus = isSolved;
    else if (selectedStatus === 'unsolved') matchStatus = !isSolved;
    else if (selectedStatus === 'revision') matchStatus = isRev;

    if (matchQuery && matchDiff && matchStatus) {
      row.style.display = '';
    } else {
      row.style.display = 'none';
    }
  });
}
