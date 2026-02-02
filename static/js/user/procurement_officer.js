document.addEventListener("DOMContentLoaded", function(){
  const ctx = document.getElementById('inboundChart');

  new Chart(ctx, {
      type: 'line',
      data: {
          labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
          datasets: [{
              label: 'Inbound Items',
              data: [120, 150, 100, 180, 200, 170, 190],
              borderWidth: 3,
              borderColor: '#2c8cfb',
              backgroundColor: 'rgba(44, 140, 251, 0.2)',
              tension: 0.4,
              fill: true,
              pointRadius: 4,
              pointBackgroundColor: '#2c8cfb'
          }]
      },
      options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
              y: { beginAtZero: true }
          }
      }
  });
});
