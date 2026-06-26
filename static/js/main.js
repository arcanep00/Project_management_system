/* =====================================================
   ProjectMS — Main JavaScript
   ===================================================== */

document.addEventListener('DOMContentLoaded', function () {

  // ---- Sidebar Toggle (mobile) ----
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebar = document.getElementById('sidebar');

  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', function () {
      sidebar.classList.toggle('show');
    });

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function (e) {
      if (window.innerWidth < 992 &&
          sidebar.classList.contains('show') &&
          !sidebar.contains(e.target) &&
          !sidebarToggle.contains(e.target)) {
        sidebar.classList.remove('show');
      }
    });
  }

  // ---- Auto-dismiss alerts after 5 seconds ----
  const alerts = document.querySelectorAll('.alert.alert-dismissible');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 5000);
  });

  // ---- Tooltip initialization ----
  const tooltipEls = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltipEls.forEach(function (el) {
    new bootstrap.Tooltip(el, { trigger: 'hover' });
  });

  // ---- Confirm delete buttons (via data-confirm attribute) ----
  document.querySelectorAll('[data-confirm]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      if (!window.confirm(this.dataset.confirm)) {
        e.preventDefault();
      }
    });
  });

  // ---- Active nav link highlight based on URL ----
  const currentPath = window.location.pathname;
  document.querySelectorAll('.sidebar .nav-link').forEach(function (link) {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });

  // ---- Table row clickable (if has data-href) ----
  document.querySelectorAll('tr[data-href]').forEach(function (row) {
    row.style.cursor = 'pointer';
    row.addEventListener('click', function () {
      window.location.href = this.dataset.href;
    });
  });

  // ---- Form validation UI (Bootstrap native) ----
  const forms = document.querySelectorAll('form[novalidate]');
  forms.forEach(function (form) {
    form.addEventListener('submit', function (e) {
      if (!form.checkValidity()) {
        e.preventDefault();
        e.stopPropagation();
      }
      form.classList.add('was-validated');
    });
  });

  // ---- Settings Nav active highlight ----
  const settingsNavLinks = document.querySelectorAll('.settings-nav-link');
  if (settingsNavLinks.length > 0) {
    window.addEventListener('scroll', function () {
      const sections = document.querySelectorAll('.settings-section');
      let current = '';
      sections.forEach(function (section) {
        const rect = section.getBoundingClientRect();
        if (rect.top <= 150) current = section.id;
      });
      settingsNavLinks.forEach(function (link) {
        link.classList.remove('active', 'bg-primary', 'bg-opacity-10');
        if (link.dataset.target === current) {
          link.classList.add('active', 'bg-primary', 'bg-opacity-10');
        }
      });
    });
  }

});
