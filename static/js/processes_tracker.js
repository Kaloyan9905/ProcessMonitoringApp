let processData = [];
let currentSort = {key: 'pid', order: true};
let currentFilter = '';
let refreshInterval = 2000;
let refreshTimeout;

async function loadData() {
    const sortKey = currentSort.key;
    const sortOrder = currentSort.order ? 'asc' : 'desc';
    const url = `/api/processes/?sort=${sortKey}&order=${sortOrder}&filter=${encodeURIComponent(currentFilter)}`;
    const response = await fetch(url);

    processData = await response.json();
    renderTable(processData);
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

function sortBy(key) {
    if (currentSort.key === key) {
        currentSort.order = !currentSort.order;
    } else {
        currentSort.key = key;
        currentSort.order = true;
    }
    loadData();
}

document.getElementById('sortPid').addEventListener('click', () => sortBy('pid'));
document.getElementById('sortName').addEventListener('click', () => sortBy('name'));
document.getElementById('sortCpu').addEventListener('click', () => sortBy('cpu_percent'));
document.getElementById('sortMem').addEventListener('click', () => sortBy('memory_percent'));

document.getElementById('filterInput').addEventListener('input', (e) => {
    currentFilter = e.target.value;
    loadData();
});

function resetFilters() {
    currentFilter = '';
    currentSort = {key: 'pid', order: true};
    document.getElementById('filterInput').value = '';
    loadData();
}

function setRefreshInterval() {
    const interval = parseInt(document.getElementById('intervalInput').value, 10);

    if (interval > 0) {
        clearInterval(refreshTimeout);
        refreshInterval = interval * 1000;
        startDataRefresh();
    }
}

function startDataRefresh() {
    loadData();
    refreshTimeout = setInterval(loadData, refreshInterval);
}

loadData();
startDataRefresh();
