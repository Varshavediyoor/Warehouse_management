document.addEventListener("DOMContentLoaded", function () {
  const ctx = document.getElementById('poStatusChart');

  new Chart(ctx, {
      type: 'line',
      data: {
          labels: [
              'PO Created',
              'Accepted',
              'In Transit',
              'Partially Received',
              'Completed'
          ],
          datasets: [{
              label: 'Purchase Orders',
              data: [60, 48, 35, 22, 40], // example values
              borderWidth: 3,
              borderColor: '#2c8cfb',
              backgroundColor: 'rgba(44, 140, 251, 0.15)',
              tension: 0.45,
              fill: true,
              pointRadius: 5,
              pointHoverRadius: 7,
              pointBackgroundColor: '#ffffff',
              pointBorderColor: '#2c8cfb',
              pointBorderWidth: 2
          }]
      },
      options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
              legend: {
                  display: true,
                  position: 'top',
                  labels: {
                      color: '#2c4c71',
                      font: {
                          size: 13,
                          weight: '600'
                      }
                  }
              },
              tooltip: {
                  backgroundColor: '#ffffff',
                  titleColor: '#2c4c71',
                  bodyColor: '#2c4c71',
                  borderColor: '#2c8cfb',
                  borderWidth: 1,
                  padding: 12,
                  callbacks: {
                      label: function (context) {
                          return ` ${context.parsed.y} Orders`;
                      }
                  }
              }
          },
          scales: {
              x: {
                  ticks: {
                      color: '#2c4c71',
                      font: {
                          size: 12,
                          weight: '500'
                      }
                  },
                  grid: {
                      display: false
                  }
              },
              y: {
                  beginAtZero: true,
                  ticks: {
                      color: '#2c4c71',
                      stepSize: 10
                  },
                  grid: {
                      color: 'rgba(44, 76, 113, 0.1)'
                  }
              }
          }
      }
  });
});
