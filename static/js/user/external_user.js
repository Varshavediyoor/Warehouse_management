const ctx = document.getElementById('chartPOvsGRN').getContext('2d');

  // Gradients
  const gradientPO = ctx.createLinearGradient(0, 0, 0, 400);
  gradientPO.addColorStop(0, 'rgba(44, 140, 251, 0.2)');
  gradientPO.addColorStop(1, 'rgba(44, 140, 251, 0.6)');

  const gradientGRN = ctx.createLinearGradient(0, 0, 0, 400);
  gradientGRN.addColorStop(0, 'rgba(165, 184, 204, 0.2)');
  gradientGRN.addColorStop(1, 'rgba(165, 184, 204, 0.6)');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      datasets: [
        {
          label: 'PO Created',
          data: [12, 9, 14, 8, 16, 11, 13],
          backgroundColor: gradientPO,
          borderRadius: 8,
          barThickness: 28
        },
        {
          label: 'GRN Received',
          data: [10, 7, 13, 6, 14, 9, 12],
          backgroundColor: gradientGRN,
          borderRadius: 8,
          barThickness: 28
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false, // ✅ Needed for fixed height
      plugins: {
        legend: {
          position: 'top',
          labels: { color: '#333', font: { size: 13, family: 'Poppins' } }
        },
        tooltip: {
          backgroundColor: 'rgba(0,0,0,0.7)',
          titleColor: '#fff',
          bodyColor: '#fff',
          cornerRadius: 8,
          padding: 10
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: '#555', font: { size: 12 } }
        },
        y: {
          grid: { color: '#eaeaea' },
          ticks: { color: '#555', font: { size: 12 } }
        }
      }
    }
  });