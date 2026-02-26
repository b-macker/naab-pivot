// NAAb Pivot Dashboard - Chart Configuration and Utilities

// Chart.js default configuration
Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
Chart.defaults.plugins.legend.display = true;
Chart.defaults.plugins.legend.position = 'top';

// Chart colors
const CHART_COLORS = {
    primary: 'rgb(102, 126, 234)',
    secondary: 'rgb(118, 75, 162)',
    success: 'rgb(76, 175, 80)',
    danger: 'rgb(244, 67, 54)',
    warning: 'rgb(255, 152, 0)',
    info: 'rgb(33, 150, 243)'
};

// Chart color schemes
const COLOR_SCHEMES = {
    speedup: [
        'rgba(255, 206, 86, 0.8)',    // Yellow (1-2x)
        'rgba(75, 192, 192, 0.8)',     // Teal (2-5x)
        'rgba(54, 162, 235, 0.8)',     // Blue (5-10x)
        'rgba(153, 102, 255, 0.8)',    // Purple (10-15x)
        'rgba(255, 99, 132, 0.8)'      // Red (15x+)
    ],
    languages: [
        'rgba(102, 126, 234, 0.8)',    // Go
        'rgba(255, 99, 71, 0.8)',      // Rust
        'rgba(0, 122, 204, 0.8)',      // C++
        'rgba(220, 20, 60, 0.8)',      // Ruby
        'rgba(240, 219, 79, 0.8)'      // JavaScript
    ]
};

// Create performance trend chart
function createPerformanceTrendChart(ctx, data) {
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels || [],
            datasets: [{
                label: 'Average Speedup',
                data: data.values || [],
                borderColor: CHART_COLORS.primary,
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                tension: 0.4,
                fill: true,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Performance Improvement Over Time',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y.toFixed(2) + 'x';
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Speedup (x)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                }
            }
        }
    });
}

// Create speedup distribution chart
function createSpeedupDistributionChart(ctx, data) {
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['1-2x', '2-5x', '5-10x', '10-15x', '15x+'],
            datasets: [{
                label: 'Number of Vessels',
                data: data || [0, 0, 0, 0, 0],
                backgroundColor: COLOR_SCHEMES.speedup,
                borderColor: COLOR_SCHEMES.speedup.map(c => c.replace('0.8', '1')),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Speedup Distribution',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return 'Vessels: ' + context.parsed.y;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Count'
                    },
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
}

// Create language distribution pie chart
function createLanguageDistributionChart(ctx, data) {
    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.labels || ['Go', 'Rust', 'C++', 'Ruby', 'JavaScript'],
            datasets: [{
                data: data.values || [0, 0, 0, 0, 0],
                backgroundColor: COLOR_SCHEMES.languages,
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Vessels by Target Language',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                },
                legend: {
                    position: 'right'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return label + ': ' + value + ' (' + percentage + '%)';
                        }
                    }
                }
            }
        }
    });
}

// Update chart with new data
function updateChart(chart, data) {
    if (!chart) return;

    if (data.labels) {
        chart.data.labels = data.labels;
    }

    if (data.datasets) {
        data.datasets.forEach((newDataset, i) => {
            if (chart.data.datasets[i]) {
                chart.data.datasets[i].data = newDataset.data;
            }
        });
    } else if (data.values) {
        chart.data.datasets[0].data = data.values;
    }

    chart.update();
}

// Export functions for use in app.js
window.ChartUtils = {
    createPerformanceTrendChart,
    createSpeedupDistributionChart,
    createLanguageDistributionChart,
    updateChart,
    CHART_COLORS,
    COLOR_SCHEMES
};
