document.addEventListener('DOMContentLoaded', function(){
  // Animate number counters
  const counters = document.querySelectorAll('[data-count]');
  counters.forEach(el => {
    const target = Number(el.dataset.count || el.textContent.replace(/[^0-9.-]+/g, ''));
    let start = 0;
    const duration = 1200;
    const stepTime = Math.max(16, Math.floor(duration / Math.abs(target - start || 1)));
    const startTime = performance.now();
    function tick(now){
      const progress = Math.min(1, (now - startTime) / duration);
      const value = Math.floor(progress * (target - start) + start);
      if(el.dataset.count && /\d{6,}/.test(String(target))){
        // format lakh/₹ style for large numbers (simple)
        if(target >= 100000) el.textContent = `₹${(value/1000).toLocaleString()} `;
        else el.textContent = value.toLocaleString();
      } else {
        el.textContent = value.toLocaleString();
      }
      if(progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  });

  // Initialize Chart.js revenue chart
  const ctx = document.getElementById('revenueChart');
  if(ctx){
    const revenueChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['Jan','Feb','Mar','Apr','May','Jun','Jul'],
        datasets: [{
          label: 'Revenue',
          data: [30000,45000,40000,65000,72000,68000,90000],
          borderColor: getComputedStyle(document.documentElement).getPropertyValue('--accent') || '#4f46e5',
          backgroundColor: 'rgba(79,70,229,0.08)',
          tension: 0.3,
          fill: true,
          pointRadius: 3
        }]
      },
      options: {
        plugins:{legend:{display:false}},
        scales:{y:{beginAtZero:true,ticks:{callback: v => '₹'+v}}}
      }
    });
    // reflow on window resize
    window.addEventListener('resize', ()=> revenueChart.resize());
  }

  // Search/filter table
  const search = document.getElementById('search');
  const table = document.getElementById('customer-table');
  const statusFilter = document.getElementById('status-filter');
  function filterTable(){
    const q = search.value.trim().toLowerCase();
    const status = statusFilter.value;
    Array.from(table.tBodies[0].rows).forEach(row => {
      const name = row.cells[0].textContent.toLowerCase();
      const email = row.cells[1].textContent.toLowerCase();
      const st = row.cells[2].textContent.toLowerCase();
      let visible = true;
      if(q && !(name.includes(q) || email.includes(q))) visible = false;
      if(status !== 'all' && st !== status) visible = false;
      row.style.display = visible ? '' : 'none';
    });
  }
  if(search) search.addEventListener('input', filterTable);
  if(statusFilter) statusFilter.addEventListener('change', filterTable);

  // Theme toggle
  const themeToggle = document.getElementById('theme-toggle');
  function setTheme(t){
    document.documentElement.setAttribute('data-theme', t);
    themeToggle.textContent = t === 'dark' ? '☀️' : '🌙';
    localStorage.setItem('theme', t);
  }
  const stored = localStorage.getItem('theme') || (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  setTheme(stored);
  themeToggle.addEventListener('click', ()=> setTheme(document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'));

  // Card detail modal
  const modal = document.getElementById('detail-modal');
  const modalTitle = document.getElementById('modal-title');
  const modalBody = document.getElementById('modal-body');
  const modalClose = document.querySelector('.modal-close');
  document.querySelectorAll('.stat.card').forEach(card => {
    card.addEventListener('click', ()=>{
      modalTitle.textContent = card.querySelector('.label').textContent;
      modalBody.textContent = card.getAttribute('data-detail') || card.querySelector('.meta')?.textContent || '';
      modal.hidden = false;
    });
  });
  modalClose.addEventListener('click', ()=> modal.hidden = true);
  modal.addEventListener('click', (e)=>{ if(e.target === modal) modal.hidden = true });
});