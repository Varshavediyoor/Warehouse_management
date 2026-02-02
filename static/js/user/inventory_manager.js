/* =========================================
   INVENTORY MANAGER – TREND CHARTS
   Warehouse Management System
========================================= */

/* ---------- GLOBAL DEFAULTS ---------- */
Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.color = "#2c4c71";
Chart.defaults.plugins.tooltip.backgroundColor = "#111827";
Chart.defaults.plugins.tooltip.titleColor = "#2c4c71";
Chart.defaults.plugins.tooltip.bodyColor = "#e5e7eb";
Chart.defaults.plugins.tooltip.padding = 10;
Chart.defaults.plugins.tooltip.cornerRadius = 8;

/* =====================================
   1️⃣ STOCK IN vs STOCK OUT
===================================== */

const stockInOutCtx = document.getElementById("stockInOutChart");

if (stockInOutCtx) {
  new Chart(stockInOutCtx, {
    type: "bar",
    data: {
      labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], // BACKEND
      datasets: [
        {
          label: "Stock In",
          data: [120, 150, 90, 170, 140, 110, 160], // BACKEND
          backgroundColor: "#b2d8ff",
          borderRadius: 8,
          barThickness: 26
        },
        {
          label: "Stock Out",
          data: [80, 100, 70, 130, 120, 90, 140], // BACKEND
          backgroundColor: "#98ccff",
          borderRadius: 8,
          barThickness: 26
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "top" }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { stepSize: 50 },
          grid: { color: "#e5e7eb" }
        },
        x: { grid: { display: false } }
      }
    }
  });
}

/* =====================================
   2️⃣ INVENTORY VALUE TREND
===================================== */

const inventoryValueCtx = document.getElementById("inventoryValueChart");

if (inventoryValueCtx) {
  new Chart(inventoryValueCtx, {
    type: "line",
    data: {
      labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"], // BACKEND
      datasets: [
        {
          label: "Inventory Value",
          data: [820000, 850000, 830000, 880000, 910000, 940000], // BACKEND
          borderColor: "#3b82f6",
          backgroundColor: "rgba(59,130,246,0.2)",
          fill: true,
          tension: 0.45,
          pointRadius: 4,
          pointBackgroundColor: "#3b82f6"
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: {
          grid: { color: "#e5e7eb" },
          ticks: {
            callback: value => `₹${value / 1000}k`
          }
        },
        x: { grid: { display: false } }
      }
    }
  });
}

/* =====================================
   3️⃣ STOCK ADJUSTMENTS TREND
===================================== */

const adjustmentsCtx = document.getElementById("adjustmentsChart");

if (adjustmentsCtx) {
  new Chart(adjustmentsCtx, {
    type: "line",
    data: {
      labels: ["Week 1", "Week 2", "Week 3", "Week 4"], // BACKEND
      datasets: [
        {
          label: "Adjustments",
          data: [12, 9, 18, 6], // BACKEND
          borderColor: "#f59e0b",
          backgroundColor: "rgba(245,158,11,0.25)",
          fill: true,
          tension: 0.5,
          pointRadius: 4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: {
          beginAtZero: true,
          grid: { color: "#e5e7eb" }
        },
        x: { grid: { display: false } }
      }
    }
  });
}

/* =====================================
   4️⃣ SLOW / DEAD STOCK %
===================================== */

const deadStockCtx = document.getElementById("deadStockChart");

if (deadStockCtx) {
  new Chart(deadStockCtx, {
    type: "doughnut",
    data: {
      labels: ["Healthy Stock", "Slow / Dead Stock"],
      datasets: [
        {
          data: [78, 22], // BACKEND
          backgroundColor: ["#5cacfa", "#aad5ff"],
          borderWidth: 0
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "72%",
      plugins: {
        legend: { position: "bottom" }
      }
    }
  });
}
