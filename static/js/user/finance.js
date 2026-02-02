Chart.defaults.font.family = "Inter, sans-serif";
Chart.defaults.color = "#374151";

/* =============================
   1. REVENUE vs OPERATIONAL COST
============================= */
new Chart(revenueCostChart, {
  type: "line",
  data: {
    labels: ["Jan","Feb","Mar","Apr","May","Jun"],
    datasets: [
      {
         label: "Revenue",
        // data: [820000, 910000, 880000, 970000, 1020000, 1100000],
          data: {
       labels: chartLabels,
       datasets: [
         { label: "Revenue", data: revenueData },
         { label: "Expenses", data: expenseData }
        ]
      },  
        borderColor: "#16a34a",
        backgroundColor: "rgba(22,163,74,0.2)",
        fill: true,
        tension: 0.4
      },
      {
        label: "Operational Cost",
        // data: [620000, 670000, 650000, 700000, 720000, 760000],
        data:[],
        borderColor: "#ef4444",
        backgroundColor: "rgba(239,68,68,0.15)",
        fill: true,
        tension: 0.4
      }
    ]
  },
  options: { responsive: true, maintainAspectRatio: false }
});

/* =============================
   2. MONTHLY PROFIT TREND
============================= */
new Chart(profitTrendChart, {
  type: "bar",
  data: {
    labels: ["Jan","Feb","Mar","Apr","May","Jun"],
    datasets: [{
      label: "Net Profit",
      // data: [200000, 240000, 230000, 270000, 300000, 340000],
      data:[],
      backgroundColor: "#22c55e",
      borderRadius: 10
    }]
  },
  options: { responsive: true, maintainAspectRatio: false }
});

/* =============================
   3. PROFITABILITY ANALYSIS
============================= */
new Chart(profitabilityChart, {
  type: "bar",
  data: {
    labels: ["Warehouse A","Warehouse B","Warehouse C"],
    datasets: [
      {
        label: "Gross Profit",
        // data: [420000, 360000, 310000],
        data:[],
        backgroundColor: "#3b82f6"
      },
      {
        label: "Net Profit",
        // data: [280000, 240000, 190000],
        data:[],
        backgroundColor: "#10b981"
      }
    ]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    borderRadius: 8
  }
});

/* =============================
   4. INVENTORY VALUE OVER TIME
============================= */
new Chart(inventoryValueChart, {
  type: "line",
  data: {
    labels: ["Jan","Feb","Mar","Apr","May","Jun"],
    datasets: [{
      label: "Inventory Value",
      // data: [5200000, 5400000, 5100000, 5600000, 5800000, 6000000],
      data:[],
      borderColor: "#0ea5e9",
      backgroundColor: "rgba(14,165,233,0.25)",
      fill: true,
      tension: 0.4
    }]
  },
  options: { responsive: true, maintainAspectRatio: false }
});

/* =============================
   5. INVENTORY HOLDING COST
============================= */
new Chart(holdingCostChart, {
  type: "doughnut",
  data: {
    labels: [
      "Storage & Space",
      "Insurance",
      "Capital Lock-in",
      "Obsolescence",
      "Damage / Expiry"
    ],
    datasets: [{
      // data: [32, 14, 26, 18, 10],
      data:[],
      backgroundColor: [
        "#3b82f6",
        "#22c55e",
        "#f59e0b",
        "#ef4444",
        "#8b5cf6"
      ]
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    cutout: "65%",
    plugins: {
      legend: { position: "bottom" }
    }
  }
});
