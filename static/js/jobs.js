// jobs.js: Apply Modal, Post Job Modal, Filter helpers

let currentApplyJobId = null;

function openApplyModal(jobId, jobTitle, companyName) {
  currentApplyJobId = jobId;
  const modal = document.getElementById('apply-job-modal');
  const titleSpan = document.getElementById('apply-modal-job-title');
  const companySpan = document.getElementById('apply-modal-company');

  if (titleSpan) titleSpan.textContent = jobTitle;
  if (companySpan) companySpan.textContent = companyName;

  if (modal) {
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }
}

function openApplyModalFromBtn(btn) {
  if (!btn) return;
  openApplyModal(btn.dataset.jobId, btn.dataset.jobTitle, btn.dataset.company);
}

function closeApplyModal() {
  const modal = document.getElementById('apply-job-modal');
  if (modal) {
    modal.classList.add('hidden');
    document.body.style.overflow = 'auto';
  }
}

function openPostJobModal() {
  const modal = document.getElementById('post-job-modal');
  if (modal) {
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }
}

function closePostJobModal() {
  const modal = document.getElementById('post-job-modal');
  if (modal) {
    modal.classList.add('hidden');
    document.body.style.overflow = 'auto';
  }
}

document.addEventListener('DOMContentLoaded', () => {
  // Apply Job Form submission
  const applyForm = document.getElementById('apply-job-form');
  if (applyForm) {
    applyForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (!currentApplyJobId) {
        showToast('Invalid job selection.', 'error');
        return;
      }

      const submitBtn = applyForm.querySelector('button[type="submit"]');
      const originalText = submitBtn.innerHTML;
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-2"></i>Submitting...';

      const formData = new FormData(applyForm);
      const payload = Object.fromEntries(formData.entries());

      try {
        const res = await fetch(`/api/jobs/${currentApplyJobId}/apply`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (data.success) {
          showToast(data.message, 'success');
          closeApplyModal();
          applyForm.reset();
        } else {
          showToast(data.error || 'Failed to submit application.', 'error');
        }
      } catch (err) {
        showToast('Network error while submitting application.', 'error');
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
      }
    });
  }

  // Post Job Form submission
  const postJobForm = document.getElementById('post-job-form');
  if (postJobForm) {
    postJobForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const submitBtn = postJobForm.querySelector('button[type="submit"]');
      const originalText = submitBtn.innerHTML;
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-2"></i>Publishing...';

      const formData = new FormData(postJobForm);
      const payload = Object.fromEntries(formData.entries());

      try {
        const res = await fetch('/api/jobs', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (data.success) {
          showToast('Job listing published successfully! Refreshing...', 'success');
          closePostJobModal();
          postJobForm.reset();
          setTimeout(() => window.location.reload(), 1200);
        } else {
          showToast(data.error || 'Failed to post job opening.', 'error');
        }
      } catch (err) {
        showToast('Network error while publishing job.', 'error');
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
      }
    });
  }
});
