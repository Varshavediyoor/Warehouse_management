document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById('inboundChart').getContext('2d');
  
    const gradient = ctx.createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, 'rgba(44,140,251,0.95)');
    gradient.addColorStop(1, 'rgba(44,140,251,0.35)');
  
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [
                'Pending Dispatch',
                'Picked Up',
                'In Transit',
                'Out for Delivery',
                'Delivered',
                'Returned'
            ],
            datasets: [{
                label: 'Shipments',
                data: [48, 82, 65, 44, 132, 9],
                backgroundColor: [
                    'rgba(255,193,7,0.85)',
                    'rgba(59,130,246,0.85)',
                    'rgba(139,92,246,0.85)',
                    'rgba(249,115,22,0.85)',
                    'rgba(34,197,94,0.9)',
                    'rgba(239,68,68,0.85)'
                ],
                borderRadius: 12,
                barPercentage: 0.6,
                categoryPercentage: 0.7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: {
                padding: {
                    top: 10,
                    left: 5,
                    right: 5,
                    bottom: 0
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: '#111827',
                    padding: 14,
                    titleFont: { size: 14, weight: '600' },
                    bodyFont: { size: 13 },
                    cornerRadius: 10
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#374151',
                        font: {
                            size: 12,
                            weight: '600'
                        }
                    }
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        borderDash: [6, 6],
                        color: 'rgba(0,0,0,0.06)'
                    },
                    ticks: {
                        color: '#6b7280',
                        font: {
                            size: 12
                        },
                        padding: 8
                    }
                }
            },
            animation: {
                duration: 1400,
                easing: 'easeOutCubic'
            }
        }
    });
  });
  