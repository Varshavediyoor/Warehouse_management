const ctx = document.getElementById('chartPOvsGRN').getContext('2d');

/* Gradients */
const gradientInbound = ctx.createLinearGradient(0, 0, 0, 400);
gradientInbound.addColorStop(0, 'rgba(44, 140, 251, 0.2)');
gradientInbound.addColorStop(1, 'rgba(44, 140, 251, 0.6)');

const gradientOutbound = ctx.createLinearGradient(0, 0, 0, 400);
gradientOutbound.addColorStop(0, 'rgba(165, 184, 204, 0.2)');
gradientOutbound.addColorStop(1, 'rgba(165, 184, 204, 0.6)');

new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [
      {
        label: 'Inbound Stock (GRN)',
        data: [120, 95, 140, 110, 160, 130, 150],
        backgroundColor: gradientInbound,
        borderRadius: 8,
        barThickness: 26
      },
      {
        label: 'Outbound Stock (Dispatch)',
        data: [90, 80, 125, 100, 145, 120, 135],
        backgroundColor: gradientOutbound,
        borderRadius: 8,
        barThickness: 26
      }
    ]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: '#333',
          font: {
            size: window.innerWidth < 480 ? 11 : 13
          }
        }
      }
    },
    scales: {
      x: {
        ticks: {
          font: {
            size: window.innerWidth < 480 ? 10 : 12
          }
        }
      },
      y: {
        ticks: {
          font: {
            size: window.innerWidth < 480 ? 10 : 12
          }
        }
      }
    }
  }
  
});




  //----------------- pie chart -------------------------------//

  const ctxUserPie = document.getElementById("userPieChart");

  new Chart(ctxUserPie, {
      type: 'doughnut',
      data: {
          labels: ["Employees", "Clients", "Admins"],
          datasets: [{
              data: [55, 30, 15], // dynamic values
              backgroundColor: ["rgba(44, 140, 251, 0.8)", "rgba(44, 140, 251, 0.4)", "rgba(165, 184, 204, 0.4)"],
              hoverBackgroundColor: ["rgba(44, 140, 251, 0.9)", "rgba(44, 140, 251, 0.6)", "rgba(165, 184, 204, 0.6)"],
              borderWidth: 2,
              borderColor: "#fff",
          }]
      },
      options: {
          responsive: true,
          cutout: "65%",
          plugins: {
              legend: { display: false },
              tooltip: { enabled: true },
              // 📌 Custom Plugin for Data Labels (%)
              datalabels: {
                  formatter: (value, ctx) => {
                      let sum = ctx.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
                      let percentage = ((value / sum) * 100).toFixed(1) + "%";
                      return percentage;
                  },
                  anchor: 'center',
                  align: 'center',
                  font: { size: 14, weight: 'bold' },
              }
          }
      },
      // 🧠 Center Text Plugin (Total count inside doughnut)
      plugins: [{
          id: 'centerText',
          afterDraw(chart) {
              const {ctx, chartArea: {width, height}} = chart;
  
              ctx.save();
              ctx.font = 'bold 18px Arial';
              ctx.textAlign = 'center';
              ctx.fillStyle = '#2c3e50';
              
              const total = chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
              ctx.fillText(`Total ${total}`, width / 2, height / 2);
              ctx.restore();
          }
      }]
  });
  
  // 🏷️ Generate Legends Dynamically
  const legendContainer = document.getElementById("chartLegend");
  const labels = ["Employees", "Clients", "Admins"];
  const colors = ["#2c8cfb", "#a5b8cc", "#5cacfa"];
  
  legendContainer.innerHTML = labels.map((label, i) => `
      <div class="legend-item">
          <span class="legend-color" style="background:${colors[i]}"></span> ${label}
      </div>
  `).join("");
  
  
  
