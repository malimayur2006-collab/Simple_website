// prep.js: Interactive Practice Quiz Engine & Notes Tabs

let quizQuestions = [];
let userAnswers = {};
let currentQuestionIndex = 0;
let quizCategory = 'aptitude';
let quizSubCategory = '';

async function startQuiz(category, subCategory = '') {
  quizCategory = category;
  quizSubCategory = subCategory;
  userAnswers = {};
  currentQuestionIndex = 0;

  const quizContainer = document.getElementById('quiz-active-container');
  const quizIntro = document.getElementById('quiz-intro-card');
  const quizSummary = document.getElementById('quiz-summary-card');

  if (quizIntro) quizIntro.classList.add('hidden');
  if (quizSummary) quizSummary.classList.add('hidden');
  if (quizContainer) {
    quizContainer.classList.remove('hidden');
    quizContainer.innerHTML = '<div class="text-center py-12"><i class="fa-solid fa-spinner fa-spin text-3xl text-indigo-400"></i><p class="mt-3 text-slate-300">Loading practice questions...</p></div>';
  }

  try {
    let url = `/api/quiz/questions?category=${encodeURIComponent(category)}`;
    if (subCategory) url += `&sub_category=${encodeURIComponent(subCategory)}`;
    
    const res = await fetch(url);
    quizQuestions = await res.json();

    if (!quizQuestions || quizQuestions.length === 0) {
      if (quizContainer) {
        quizContainer.innerHTML = `
          <div class="text-center py-10 bg-slate-800/80 rounded-xl border border-slate-700">
            <i class="fa-solid fa-folder-open text-4xl text-slate-500 mb-3"></i>
            <h3 class="text-lg font-semibold text-slate-200">No questions found for this topic yet</h3>
            <p class="text-sm text-slate-400 mt-1">Please try another category or check back soon!</p>
            <button onclick="resetQuiz()" class="mt-4 px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm hover:bg-indigo-500 transition">Back to Categories</button>
          </div>
        `;
      }
      return;
    }

    renderCurrentQuestion();
  } catch (err) {
    if (quizContainer) {
      quizContainer.innerHTML = '<div class="text-center text-rose-400 py-8">Failed to load quiz questions. Please try again.</div>';
    }
  }
}

function renderCurrentQuestion() {
  const container = document.getElementById('quiz-active-container');
  if (!container || quizQuestions.length === 0) return;

  const q = quizQuestions[currentQuestionIndex];
  const selectedOption = userAnswers[q.id] || null;

  container.innerHTML = `
    <div class="bg-slate-800/90 border border-slate-700 rounded-2xl p-6 sm:p-8 shadow-xl">
      <!-- Header / Progress -->
      <div class="flex items-center justify-between pb-4 border-b border-slate-700/80 mb-6">
        <div class="flex items-center space-x-3">
          <span class="px-3 py-1 text-xs rounded-full bg-indigo-500/20 text-indigo-300 font-semibold uppercase">${q.category} &bull; ${q.sub_category}</span>
          <span class="text-xs px-2.5 py-0.5 rounded-full ${
            q.difficulty === 'Easy' ? 'bg-emerald-500/20 text-emerald-300' :
            q.difficulty === 'Medium' ? 'bg-amber-500/20 text-amber-300' : 'bg-rose-500/20 text-rose-300'
          }">${q.difficulty}</span>
        </div>
        <div class="text-sm font-medium text-slate-400 font-mono">
          Question <span class="text-white font-bold">${currentQuestionIndex + 1}</span> of ${quizQuestions.length}
        </div>
      </div>

      <!-- Question Text -->
      <h3 class="text-lg sm:text-xl font-semibold text-slate-100 leading-relaxed mb-6">
        ${q.question}
      </h3>

      <!-- Options -->
      <div class="space-y-3 mb-8">
        ${['A', 'B', 'C', 'D'].map(optKey => {
          const optText = q[`option_${optKey.toLowerCase()}`];
          const isSelected = selectedOption === optKey;
          return `
            <div onclick="selectQuizOption(${q.id}, '${optKey}')" 
                 class="flex items-center p-4 rounded-xl border cursor-pointer transition ${
                   isSelected
                     ? 'bg-indigo-600/30 border-indigo-500 text-white shadow-md shadow-indigo-500/10'
                     : 'bg-slate-900/60 border-slate-700 text-slate-300 hover:bg-slate-700/50 hover:border-slate-600'
                 }">
              <div class="w-8 h-8 rounded-lg flex items-center justify-center font-bold text-sm mr-4 ${
                isSelected ? 'bg-indigo-500 text-white' : 'bg-slate-800 text-slate-400 border border-slate-700'
              }">${optKey}</div>
              <div class="text-sm sm:text-base flex-1">${optText}</div>
            </div>
          `;
        }).join('')}
      </div>

      <!-- Actions -->
      <div class="flex items-center justify-between pt-4 border-t border-slate-700/80">
        <button onclick="prevQuestion()" ${currentQuestionIndex === 0 ? 'disabled' : ''} 
                class="px-4 py-2 rounded-lg border border-slate-700 text-slate-300 hover:bg-slate-700 transition text-sm font-medium disabled:opacity-40 disabled:cursor-not-allowed">
          <i class="fa-solid fa-arrow-left mr-2"></i> Previous
        </button>

        <div class="flex items-center space-x-3">
          ${currentQuestionIndex === quizQuestions.length - 1 ? `
            <button onclick="submitQuiz()" class="px-6 py-2.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-sm shadow-lg shadow-emerald-600/20 transition flex items-center">
              <i class="fa-solid fa-check-double mr-2"></i> Submit & Finish Quiz
            </button>
          ` : `
            <button onclick="nextQuestion()" class="px-5 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm transition flex items-center">
              Next <i class="fa-solid fa-arrow-right ml-2"></i>
            </button>
          `}
        </div>
      </div>
    </div>
  `;
}

function selectQuizOption(questionId, optionKey) {
  userAnswers[questionId] = optionKey;
  renderCurrentQuestion();
}

function prevQuestion() {
  if (currentQuestionIndex > 0) {
    currentQuestionIndex--;
    renderCurrentQuestion();
  }
}

function nextQuestion() {
  if (currentQuestionIndex < quizQuestions.length - 1) {
    currentQuestionIndex++;
    renderCurrentQuestion();
  }
}

async function submitQuiz() {
  const answeredCount = Object.keys(userAnswers).length;
  if (answeredCount < quizQuestions.length) {
    if (!confirm(`You have answered ${answeredCount} of ${quizQuestions.length} questions. Submit anyway?`)) {
      return;
    }
  }

  const container = document.getElementById('quiz-active-container');
  if (container) {
    container.innerHTML = '<div class="text-center py-12"><i class="fa-solid fa-spinner fa-spin text-3xl text-emerald-400"></i><p class="mt-3 text-slate-300">Calculating your results and score...</p></div>';
  }

  try {
    const res = await fetch('/api/quiz/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        answers: userAnswers,
        category: quizCategory,
        sub_category: quizSubCategory || 'All'
      })
    });

    const data = await res.json();
    renderQuizSummary(data);
  } catch (err) {
    showToast('Failed to evaluate quiz results.', 'error');
  }
}

function renderQuizSummary(data) {
  const container = document.getElementById('quiz-active-container');
  const summary = document.getElementById('quiz-summary-card');
  if (container) container.classList.add('hidden');
  if (!summary) return;

  summary.classList.remove('hidden');

  const scorePct = data.percentage || 0;
  let statusBadge = '';
  if (scorePct >= 80) statusBadge = '<span class="text-emerald-400 font-bold">Outstanding! Exam Ready 🚀</span>';
  else if (scorePct >= 50) statusBadge = '<span class="text-amber-400 font-bold">Good effort! A little more revision needed 💡</span>';
  else statusBadge = '<span class="text-rose-400 font-bold">Needs more practice! Review notes carefully 📚</span>';

  summary.innerHTML = `
    <div class="bg-slate-800/90 border border-slate-700 rounded-2xl p-6 sm:p-8 shadow-2xl">
      <div class="text-center pb-6 border-b border-slate-700">
        <div class="inline-flex items-center justify-center w-20 h-20 rounded-full bg-indigo-500/20 border-2 border-indigo-500/40 text-indigo-400 mb-4 text-3xl font-bold font-mono">
          ${scorePct}%
        </div>
        <h2 class="text-2xl font-bold text-white">Quiz Evaluation Completed</h2>
        <p class="text-slate-300 text-sm mt-1">You scored <strong class="text-white">${data.score}</strong> out of <strong class="text-white">${data.total}</strong> correct (${statusBadge})</p>
        <div class="mt-4 flex justify-center space-x-3">
          <button onclick="startQuiz('${quizCategory}', '${quizSubCategory}')" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-semibold transition">
            <i class="fa-solid fa-rotate-right mr-2"></i> Retake Quiz
          </button>
          <button onclick="resetQuiz()" class="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-slate-200 rounded-lg text-sm font-medium transition">
            Browse All Prep Notes
          </button>
        </div>
      </div>

      <!-- Detailed Review with Explanations -->
      <div class="mt-6">
        <h3 class="text-lg font-bold text-slate-200 mb-4 flex items-center">
          <i class="fa-solid fa-list-check text-indigo-400 mr-2"></i> Detailed Solution & Explanations
        </h3>
        <div class="space-y-4">
          ${data.results.map((res, idx) => `
            <div class="p-4 rounded-xl border ${res.is_correct ? 'bg-emerald-950/20 border-emerald-500/40' : 'bg-rose-950/20 border-rose-500/40'}">
              <div class="flex items-start justify-between">
                <span class="text-xs font-mono font-bold px-2 py-0.5 rounded ${res.is_correct ? 'bg-emerald-500/20 text-emerald-300' : 'bg-rose-500/20 text-rose-300'}">
                  Q${idx + 1} &bull; ${res.is_correct ? 'Correct' : 'Incorrect'}
                </span>
                <span class="text-xs text-slate-400">Your choice: <strong class="${res.is_correct ? 'text-emerald-400' : 'text-rose-400'}">${res.selected || 'Unanswered'}</strong> | Correct: <strong class="text-emerald-400">${res.correct}</strong></span>
              </div>
              <p class="text-slate-200 font-medium text-sm mt-2">${res.question}</p>
              <div class="mt-3 p-3 bg-slate-900/80 rounded-lg border border-slate-800 text-xs text-slate-300 leading-relaxed">
                <strong class="text-indigo-400">Explanation:</strong> ${res.explanation}
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    </div>
  `;
}

function resetQuiz() {
  const quizContainer = document.getElementById('quiz-active-container');
  const quizIntro = document.getElementById('quiz-intro-card');
  const quizSummary = document.getElementById('quiz-summary-card');

  if (quizContainer) quizContainer.classList.add('hidden');
  if (quizSummary) quizSummary.classList.add('hidden');
  if (quizIntro) quizIntro.classList.remove('hidden');
}
