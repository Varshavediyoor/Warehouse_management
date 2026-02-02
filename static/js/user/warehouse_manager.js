Chart.defaults.font.family = "Inter, sans-serif";
Chart.defaults.color = "#374151";

/* =============================
   INBOUND vs PUTAWAY
============================= */
new Chart(inboundPutawayChart, {
  type: "line",
  data: {
    labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    datasets: [
      {
        label: "Inbound",
        data: [120, 150, 90, 170, 140, 160],
        borderColor: "#3b82f6",
        backgroundColor: "rgba(59,130,246,0.15)",
        tension: 0.4,
        fill: true
      },
      {
        label: "Putaway",
        data: [100, 130, 80, 150, 120, 140],
        borderColor: "#22c55e",
        backgroundColor: "rgba(34,197,94,0.15)",
        tension: 0.4,
        fill: true
      }
    ]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false
  }
});

/* =============================
   QC PASS / FAIL
============================= */
new Chart(qcTrendChart, {
  type: "bar",
  data: {
    labels: ["Mon", "Tue", "Wed", "Thu", "Fri"],
    datasets: [
      { label: "QC Pass", data: [95,110,105,120,115], backgroundColor: "#98ccff" },
      { label: "QC Fail", data: [8,6,9,5,7], backgroundColor: "#E03F3F" }
    ]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    borderRadius: 8
  }
});

/* =============================
   INVENTORY AGING (FIXED)
============================= */
new Chart(agingChart, {
  type: "doughnut",
  data: {
    labels: ["0–30 Days", "31–60 Days", "61–90 Days", "90+ Days"],
    datasets: [{
      data: [55, 25, 12, 8],
      backgroundColor: ["#22c55e", "#3b82f6", "#f59e0b", "#ef4444"]
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    cutout: "65%",
    plugins: { legend: { position: "bottom" } }
  }
});

/* =============================
   ORDER FULFILMENT
============================= */
new Chart(fulfilmentChart, {
  type: "line",
  data: {
    labels: ["Week 1", "Week 2", "Week 3", "Week 4"],
    datasets: [{
      label: "Fulfilment %",
      data: [92, 94, 96, 95],
      borderColor: "#0ea5e9",
      backgroundColor: "rgba(14,165,233,0.2)",
      tension: 0.4,
      fill: true
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        min: 85,
        max: 100,
        ticks: { callback: v => v + "%" }
      }
    }
  }
});
