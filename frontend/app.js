async function api(path, options = {}) {
    const response = await fetch(path, {
        headers: { 'Content-Type': 'application/json' },
        ...options,
    });

    if (!response.ok) {
        const text = await response.text();
        throw new Error(text || `HTTP ${response.status}`);
    }

    return response.json();
}

function renderInfo(data) {
    document.getElementById('infoBox').innerHTML = `
        <div><strong>service:</strong> <code>${data.service}</code></div>
        <div><strong>hostname:</strong> <code>${data.hostname}</code></div>
        <div><strong>db:</strong> <code>${data.db_status}</code></div>
        <div><strong>time:</strong> <code>${data.timestamp}</code></div>
    `;
}

function renderItems(data) {
    document.getElementById('itemsReplica').innerText = `backend: ${data.backend_hostname}`;

    if (!data.items.length) {
        document.getElementById('itemsBox').innerHTML = '<div class="text-muted">Пока записей нет.</div>';
        return;
    }

    const html = data.items.map(item => `
        <li class="list-group-item d-flex justify-content-between align-items-start">
            <div>
                <div>${item.text}</div>
                <div class="small text-muted">id=${item.id}</div>
            </div>
            <span class="badge text-bg-light mono">${item.created_at}</span>
        </li>
    `).join('');

    document.getElementById('itemsBox').innerHTML = `<ul class="list-group">${html}</ul>`;
}

async function loadInfo() {
    const data = await api('/api/info');
    renderInfo(data);
}

async function loadItems() {
    const data = await api('/api/items');
    renderItems(data);
}

async function runMl() {
    const x = document.getElementById('mlInput').value || 0;
    const data = await api(`/api/ml-proxy?x=${encodeURIComponent(x)}`);

    document.getElementById('mlBox').innerHTML = `
        <div><strong>score:</strong> <code>${data.score}</code></div>
        <div><strong>backend:</strong> <code>${data.backend_hostname}</code></div>
        <div><strong>gpu_node:</strong> <code>${data.gpu_node}</code></div>
        <div><strong>explanation:</strong> ${data.explanation}</div>
    `;
}

async function runHeavy() {
    const seconds = document.getElementById('heavySeconds').value || 1;
    const box = document.getElementById('heavyBox');

    box.innerHTML = 'Выполняется CPU-нагрузка...';

    const data = await api(`/api/heavy?seconds=${encodeURIComponent(seconds)}`);
    box.innerHTML = `
        <div><strong>status:</strong> <code>${data.status}</code></div>
        <div><strong>backend:</strong> <code>${data.backend_hostname}</code></div>
        <div><strong>seconds:</strong> <code>${data.seconds}</code></div>
        <div><strong>iterations:</strong> <code>${data.iterations}</code></div>
        <div><strong>resource_hint:</strong> ${data.resource_hint}</div>
    `;
}

async function runMemory() {
    const megabytes = document.getElementById('memoryMegabytes').value || 1;
    const holdSeconds = document.getElementById('memoryHoldSeconds').value || 1;
    const box = document.getElementById('memoryBox');

    box.innerHTML = 'Выделяется память...';

    const data = await api(
        `/api/memory?megabytes=${encodeURIComponent(megabytes)}&hold_seconds=${encodeURIComponent(holdSeconds)}`
    );

    box.innerHTML = `
        <div><strong>status:</strong> <code>${data.status}</code></div>
        <div><strong>backend:</strong> <code>${data.backend_hostname}</code></div>
        <div><strong>requested_mb:</strong> <code>${data.requested_mb}</code></div>
        <div><strong>allocated_mb:</strong> <code>${data.allocated_mb}</code></div>
        <div><strong>hold_seconds:</strong> <code>${data.hold_seconds}</code></div>
        <div><strong>resource_hint:</strong> ${data.resource_hint}</div>
    `;
}

async function runThreads() {
    const threads = document.getElementById('threadsCount').value || 1;
    const seconds = document.getElementById('threadsSeconds').value || 1;
    const box = document.getElementById('threadsBox');

    box.innerHTML = 'Запускаются потоки...';

    const data = await api(
        `/api/threads?threads=${encodeURIComponent(threads)}&seconds=${encodeURIComponent(seconds)}`
    );

    box.innerHTML = `
        <div><strong>status:</strong> <code>${data.status}</code></div>
        <div><strong>backend:</strong> <code>${data.backend_hostname}</code></div>
        <div><strong>threads_requested:</strong> <code>${data.threads_requested}</code></div>
        <div><strong>seconds:</strong> <code>${data.seconds}</code></div>
        <div><strong>iterations:</strong> <code>${data.iterations}</code></div>
        <div><strong>threads_before:</strong> <code>${data.threads_before}</code></div>
        <div><strong>threads_after:</strong> <code>${data.threads_after}</code></div>
        <div><strong>resource_hint:</strong> ${data.resource_hint}</div>
    `;
}

async function addItem(evt) {
    evt.preventDefault();

    const input = document.getElementById('itemText');
    const formStatus = document.getElementById('formStatus');
    const text = input.value.trim();

    if (!text) return;

    try {
        const data = await api('/api/items', {
            method: 'POST',
            body: JSON.stringify({ text }),
        });

        formStatus.innerHTML = `Добавлено через backend <code>${data.backend_hostname}</code>`;
        input.value = '';
        await loadItems();
    } catch (error) {
        formStatus.textContent = `Ошибка: ${error.message}`;
    }
}

async function loadAll() {
    try {
        await Promise.all([loadInfo(), loadItems()]);
    } catch (error) {
        document.getElementById('infoBox').textContent = `Ошибка загрузки: ${error.message}`;
        document.getElementById('itemsBox').textContent = `Ошибка загрузки: ${error.message}`;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const refreshBtn = document.getElementById('refreshBtn');
    const mlBtn = document.getElementById('mlBtn');
    const heavyBtn = document.getElementById('heavyBtn');
    const memoryBtn = document.getElementById('memoryBtn');
    const threadsBtn = document.getElementById('threadsBtn');
    const itemForm = document.getElementById('itemForm');

    refreshBtn?.addEventListener('click', loadAll);

    mlBtn?.addEventListener('click', async () => {
        try {
            await runMl();
        } catch (error) {
            document.getElementById('mlBox').textContent = error.message;
        }
    });

    heavyBtn?.addEventListener('click', async () => {
        try {
            await runHeavy();
        } catch (error) {
            document.getElementById('heavyBox').textContent = error.message;
        }
    });

    memoryBtn?.addEventListener('click', async () => {
        try {
            await runMemory();
        } catch (error) {
            document.getElementById('memoryBox').textContent = error.message;
        }
    });

    threadsBtn?.addEventListener('click', async () => {
        try {
            await runThreads();
        } catch (error) {
            document.getElementById('threadsBox').textContent = error.message;
        }
    });

    itemForm?.addEventListener('submit', addItem);

    loadAll();
});