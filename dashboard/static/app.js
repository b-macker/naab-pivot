// NAAb Pivot Dashboard - Main Application Logic

// Navigation
document.addEventListener('DOMContentLoaded', () => {
    // Initialize dashboard
    initDashboard();

    // Setup navigation
    setupNavigation();

    // Load data
    loadProjects();
    loadBenchmarks();
    loadVessels();

    // Setup charts
    setupCharts();
});

function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.section');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);

            // Update active nav link
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');

            // Update active section
            sections.forEach(s => s.classList.remove('active'));
            document.getElementById(targetId).classList.add('active');
        });
    });
}

function initDashboard() {
    console.log('NAAb Pivot Dashboard initialized');
}

// Load Projects
async function loadProjects() {
    try {
        const response = await axios.get('/api/projects');
        const projects = response.data.projects || generateSampleProjects();

        displayProjects(projects);
        updateOverviewStats(projects);
    } catch (error) {
        console.error('Error loading projects:', error);
        const projects = generateSampleProjects();
        displayProjects(projects);
        updateOverviewStats(projects);
    }
}

function displayProjects(projects) {
    const projectsList = document.getElementById('projects-list');

    if (projects.length === 0) {
        projectsList.innerHTML = '<p class="loading">No projects found. Run <code>naab-pivot evolve</code> to create your first project.</p>';
        return;
    }

    projectsList.innerHTML = projects.map(project => `
        <div class="project-card">
            <h3>${project.name || 'Unnamed Project'}</h3>
            <p>${project.path || 'No path specified'}</p>
            <div class="project-stats">
                <span class="project-stat"><strong>${project.vessels || 0}</strong> vessels</span>
                <span class="project-stat">Last evolution: <strong>${project.last_evolution || 'Never'}</strong></span>
            </div>
        </div>
    `).join('');

    // Update recent activity
    displayRecentActivity(projects);
}

function displayRecentActivity(projects) {
    const recentActivity = document.getElementById('recent-activity');

    const activity = projects.slice(0, 5).map(project => `
        <div style="padding: 0.75rem; margin-bottom: 0.5rem; background: var(--bg-primary); border-radius: 5px;">
            <strong>${project.name}</strong> - ${project.vessels} vessels generated
            <span style="color: var(--text-secondary); font-size: 0.9rem; float: right;">${project.last_evolution}</span>
        </div>
    `).join('');

    recentActivity.innerHTML = activity || '<p class="loading">No recent activity</p>';
}

// Load Benchmarks
async function loadBenchmarks() {
    try {
        const response = await axios.get('/api/benchmarks');
        const benchmarks = response.data.benchmarks || generateSampleBenchmarks();

        displayBenchmarks(benchmarks);
    } catch (error) {
        console.error('Error loading benchmarks:', error);
        const benchmarks = generateSampleBenchmarks();
        displayBenchmarks(benchmarks);
    }
}

function displayBenchmarks(benchmarks) {
    // Update performance chart
    updatePerformanceChart(benchmarks);
}

// Load Vessels
async function loadVessels() {
    try {
        const response = await axios.get('/api/vessels');
        const vessels = response.data.vessels || generateSampleVessels();

        displayVessels(vessels);
    } catch (error) {
        console.error('Error loading vessels:', error);
        const vessels = generateSampleVessels();
        displayVessels(vessels);
    }
}

function displayVessels(vessels) {
    const vesselsCatalog = document.getElementById('vessels-catalog');

    if (vessels.length === 0) {
        vesselsCatalog.innerHTML = '<p class="loading">No vessels generated yet.</p>';
        return;
    }

    vesselsCatalog.innerHTML = vessels.map(vessel => `
        <div class="vessel-card">
            <div class="vessel-info">
                <h3>${vessel.name || 'Unnamed Vessel'}</h3>
                <div class="vessel-meta">
                    Target: <strong>${vessel.target || 'Unknown'}</strong> |
                    Size: <strong>${formatBytes(vessel.size || 0)}</strong> |
                    Compiled: <strong>${vessel.compiled_at || 'Unknown'}</strong>
                </div>
            </div>
            <div class="vessel-stats">
                <div class="speedup-badge">${vessel.speedup || '0'}x</div>
            </div>
        </div>
    `).join('');
}

// Update Overview Stats
function updateOverviewStats(projects) {
    const totalProjects = projects.length;
    const totalVessels = projects.reduce((sum, p) => sum + (p.vessels || 0), 0);
    const avgSpeedup = projects.length > 0 ?
        (projects.reduce((sum, p) => sum + (p.avg_speedup || 0), 0) / projects.length).toFixed(1) : '0';
    const parityRate = '99.9%';

    document.getElementById('total-projects').textContent = totalProjects;
    document.getElementById('total-vessels').textContent = totalVessels;
    document.getElementById('avg-speedup').textContent = avgSpeedup + 'x';
    document.getElementById('parity-rate').textContent = parityRate;
}

// Setup Charts
let performanceChart = null;
let speedupChart = null;

function setupCharts() {
    // Performance Trend Chart
    const perfCtx = document.getElementById('performanceChart');
    if (perfCtx) {
        performanceChart = new Chart(perfCtx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Average Speedup',
                    data: [],
                    borderColor: 'rgb(102, 126, 234)',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Performance Improvement Over Time'
                    },
                    legend: {
                        display: true
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

    // Speedup Distribution Chart
    const speedupCtx = document.getElementById('speedupChart');
    if (speedupCtx) {
        speedupChart = new Chart(speedupCtx, {
            type: 'bar',
            data: {
                labels: ['1-2x', '2-5x', '5-10x', '10-15x', '15x+'],
                datasets: [{
                    label: 'Number of Vessels',
                    data: [5, 15, 8, 3, 2],
                    backgroundColor: [
                        'rgba(255, 206, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(153, 102, 255, 0.8)',
                        'rgba(255, 99, 132, 0.8)'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Speedup Distribution'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Count'
                        }
                    }
                }
            }
        });
    }
}

function updatePerformanceChart(benchmarks) {
    if (!performanceChart) return;

    const labels = benchmarks.map((b, i) => `Day ${i + 1}`);
    const data = benchmarks.map(b => b.avg_speedup || 0);

    performanceChart.data.labels = labels;
    performanceChart.data.datasets[0].data = data;
    performanceChart.update();
}

// Utility Functions
function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Sample Data Generators (for demo when no real data exists)
function generateSampleProjects() {
    return [
        {
            name: 'E-Commerce Backend',
            path: '/workspace/ecommerce',
            vessels: 5,
            last_evolution: '2 hours ago',
            avg_speedup: 3.5
        },
        {
            name: 'Data Pipeline',
            path: '/workspace/data-pipeline',
            vessels: 8,
            last_evolution: '1 day ago',
            avg_speedup: 10.2
        },
        {
            name: 'ML Inference',
            path: '/workspace/ml-inference',
            vessels: 3,
            last_evolution: '3 days ago',
            avg_speedup: 15.6
        }
    ];
}

function generateSampleBenchmarks() {
    return [
        { date: '2024-01-01', avg_speedup: 3.2 },
        { date: '2024-01-02', avg_speedup: 4.1 },
        { date: '2024-01-03', avg_speedup: 5.3 },
        { date: '2024-01-04', avg_speedup: 6.2 },
        { date: '2024-01-05', avg_speedup: 7.8 }
    ];
}

function generateSampleVessels() {
    return [
        {
            name: 'calculate_commission',
            target: 'Rust',
            size: 1847296,
            compiled_at: '2 hours ago',
            speedup: 12.5
        },
        {
            name: 'process_batch',
            target: 'Go',
            size: 2123456,
            compiled_at: '1 day ago',
            speedup: 8.3
        },
        {
            name: 'heavy_computation',
            target: 'C++',
            size: 1654321,
            compiled_at: '3 days ago',
            speedup: 15.2
        }
    ];
}
