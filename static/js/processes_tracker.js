let processData = [];
let currentSort = { key: 'pid', order: true };
let currentFilter = '';
let refreshInterval = 2000;
let refreshTimer;

async function loadData() {
    const sortKey = currentSort.key;
    const sortOrder = currentSort.order ? 'asc' : 'desc';
    const url = `/api/processes/?sort=${sortKey}&order=${sortOrder}&filter=${encodeURIComponent(currentFilter)}`;

    try {
        const response = await fetch(url);
        processData = await response.json();
        renderTable(processData);
    } catch (error) {
        console.error("Error loading process data:", error);
    }
}

function renderTable(data) {
    const table = document.getElementById('processTable');
    const fragment = document.createDocumentFragment();

    data.forEach((proc, index) => {
        const row = document.createElement('tr');
        row.classList.add(index % 2 === 0 ? 'bg-gray-50' : 'bg-gray-100');
        row.innerHTML = `
            <td class="border px-4 py-3">${proc.pid}</td>
            <td class="border px-4 py-3">${proc.name}</td>
            <td class="border px-4 py-3">${proc.cpu_percent}</td>
            <td class="border px-4 py-3">${proc.memory_percent.toFixed(2)}</td>
        `;
        fragment.appendChild(row);
    });

    table.innerHTML = '';
    table.appendChild(fragment);
}

let debounceTimeout;

async function fetchAlerts() {
    if (debounceTimeout) {
        clearTimeout(debounceTimeout);
    }

    debounceTimeout = setTimeout(async () => {
        try {
            const response = await fetch('/api/anomalies/');
            const alerts = await response.json();
            console.log(alerts);

            if (alerts.length > 0) {
                alerts.forEach(alert => {
                    Toastify({
                        text: `${alert.title}: ${alert.message}`,
                        duration: 5000,
                        backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
                    }).showToast();
                });
            }
        } catch (error) {
            console.error("Error fetching alerts:", error);
        }
    }, 1000);
}

function sortBy(key) {
    if (currentSort.key === key) {
        currentSort.order = !currentSort.order;
    } else {
        currentSort.key = key;
        currentSort.order = true;
    }
    loadData();
}

function resetFilters() {
    currentFilter = '';
    currentSort = { key: 'pid', order: true };
    document.getElementById('filterInput').value = '';
    loadData();
}

function setRefreshInterval() {
    const interval = parseInt(document.getElementById('intervalInput').value, 10);
    if (interval > 0) {
        clearInterval(refreshTimer);
        refreshInterval = interval * 1000;
        startDataRefresh();
    }
}

function startDataRefresh() {
    loadData();
    fetchAlerts();
    refreshTimer = setInterval(() => {
        loadData();
        fetchAlerts();
    }, refreshInterval);
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('sortPid').addEventListener('click', () => sortBy('pid'));
    document.getElementById('sortName').addEventListener('click', () => sortBy('name'));
    document.getElementById('sortCpu').addEventListener('click', () => sortBy('cpu_percent'));
    document.getElementById('sortMem').addEventListener('click', () => sortBy('memory_percent'));

    document.getElementById('filterInput').addEventListener('input', (e) => {
        currentFilter = e.target.value;
        loadData();
    });

    document.getElementById('intervalInput')?.addEventListener('change', setRefreshInterval);

    startDataRefresh();
});
