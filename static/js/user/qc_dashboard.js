const pieCtx = document.getElementById('qcPieChart').getContext('2d');

const passGradient = pieCtx.createLinearGradient(0, 0, 0, 200);
passGradient.addColorStop(0, '#4ade80');
passGradient.addColorStop(1, '#16a34a');

const failGradient = pieCtx.createLinearGradient(0, 0, 0, 200);
failGradient.addColorStop(0, '#f87171');
failGradient.addColorStop(1, '#b91c1c');

/* SHADOW PLUGIN – 3D EFFECT */
const shadowPlugin = {
  id: 'shadow',
  beforeDraw(chart) {
    const ctx = chart.ctx;
    ctx.save();
    ctx.shadowColor = 'rgba(0,0,0,0.25)';
    ctx.shadowBlur = 12;
    ctx.shadowOffsetY = 6;
  },
  afterDraw(chart) {
    chart.ctx.restore();
  }
};

new Chart(pieCtx, {
  type: 'pie',   // ✅ PURE PIE
  data: {
    labels: ['QC Passed', 'QC Failed'],
    datasets: [{
      data: [78, 22],
      backgroundColor: [passGradient, failGradient],
      borderWidth: 2,
      borderColor: '#ffffff',
      hoverOffset: 12
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,

    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          font: {
            size: 10,
            weight: '600'
          },
          padding: 12,
          boxWidth: 10
        }
      },
      tooltip: {
        bodyFont: { size: 11 },
        callbacks: {
          label: ctx => `${ctx.label}: ${ctx.raw}%`
        }
      }
    }
  },
  plugins: [shadowPlugin]
});


/* ===============================
   LINE CHART – QC TREND
================================ */

const lineCtx = document.getElementById('qcLineChart').getContext('2d');

const lineGradient = lineCtx.createLinearGradient(0, 0, 0, 220);
lineGradient.addColorStop(0, 'rgba(59,130,246,0.35)');
lineGradient.addColorStop(1, 'rgba(59,130,246,0.03)');

new Chart(lineCtx, {
  type: 'line',
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [{
      label: 'QC Pass Rate',
      data: [82, 78, 85, 88, 91, 94],
      fill: true,
      backgroundColor: lineGradient,
      borderColor: '#2563eb',
      borderWidth: 2,          // 🔽 thinner line
      tension: 0.4,
      pointRadius: 3,         // 🔽 smaller points
      pointHoverRadius: 4,
      pointBackgroundColor: '#2563eb'
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,  // IMPORTANT for small cards

    plugins: {
      legend: {
        display: true,
        labels: {
          font: {
            size: 11,           // 🔽 smaller legend font
            weight: '500'
          },
          boxWidth: 10
        }
      },
      tooltip: {
        titleFont: { size: 11 },
        bodyFont: { size: 11 }
      }
    },

    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          font: {
            size: 10           // 🔽 smaller Y-axis labels
          },
          callback: value => value + '%'
        },
        grid: {
          drawBorder: false
        }
      },
      x: {
        ticks: {
          font: {
            size: 10           // 🔽 smaller X-axis labels
          }
        },
        grid: {
          display: false
        }
      }
    }
  }
});
