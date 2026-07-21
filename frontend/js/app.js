// ===== PyAssistant Analytics - Frontend Application =====

const API_BASE = window.location.origin + '/api';
let currentLang = 'es';
let dailyChart = null;
let categoriesChart = null;

// ===== i18n Translations =====
const i18n = {
    es: {
        overview: 'Resumen',
        daily: 'Tendencia Diaria',
        categories: 'Por Categoría',
        chat: 'Chat con IA',
        add: 'Agregar',
        overviewTitle: 'Resumen General',
        overviewSubtitle: 'Tu productividad en los últimos 30 días',
        totalActivities: 'Actividades totales',
        totalHours: 'Horas totales',
        avgScore: 'Productividad promedio',
        bestDay: 'Mejor día',
        aiInsights: 'Insights de IA',
        generate: 'Generar análisis',
        insightsPlaceholder: 'Haz clic en "Generar análisis" para obtener insights personalizados sobre tu productividad usando IA.',
        dailyTitle: 'Tendencia Diaria',
        dailySubtitle: 'Últimos 7 días',
        categoriesTitle: 'Distribución por Categoría',
        categoriesSubtitle: 'En qué estás invirtiendo tu tiempo',
        chatTitle: 'Chat con tu Asistente IA',
        chatSubtitle: 'Pregunta lo que quieras sobre tu productividad',
        chatWelcome: '¡Hola! Soy tu asistente de productividad. Pregúntame sobre tus datos. Por ejemplo:',
        chatExample1: '¿Cuál fue mi mejor semana?',
        chatExample2: '¿En qué categoría gasto más tiempo?',
        chatExample3: '¿Cuánto tiempo dediqué a aprender este mes?',
        send: 'Enviar',
        chatPlaceholder: 'Escribe tu pregunta aquí...',
        addTitle: 'Agregar Nueva Actividad',
        title: 'Título',
        description: 'Descripción',
        category: 'Categoría',
        duration: 'Duración (minutos)',
        startTime: 'Fecha y hora de inicio',
        productivity: 'Productividad (1-10)',
        save: 'Guardar Actividad',
        recentActivities: 'Actividades Recientes',
        madeWith: 'Hecho con FastAPI + Gemini + Chart.js',
    },
    en: {
        overview: 'Overview',
        daily: 'Daily Trend',
        categories: 'By Category',
        chat: 'AI Chat',
        add: 'Add',
        overviewTitle: 'Overview',
        overviewSubtitle: 'Your productivity in the last 30 days',
        totalActivities: 'Total activities',
        totalHours: 'Total hours',
        avgScore: 'Average productivity',
        bestDay: 'Best day',
        aiInsights: 'AI Insights',
        generate: 'Generate analysis',
        insightsPlaceholder: 'Click "Generate analysis" to get personalized productivity insights using AI.',
        dailyTitle: 'Daily Trend',
        dailySubtitle: 'Last 7 days',
        categoriesTitle: 'Distribution by Category',
        categoriesSubtitle: 'Where you are investing your time',
        chatTitle: 'Chat with your AI Assistant',
        chatSubtitle: 'Ask anything about your productivity',
        chatWelcome: 'Hi! I\'m your productivity assistant. Ask me about your data. For example:',
        chatExample1: 'What was my best week?',
        chatExample2: 'Which category takes most of my time?',
        chatExample3: 'How much time did I spend learning this month?',
        send: 'Send',
        chatPlaceholder: 'Type your question here...',
        addTitle: 'Add New Activity',
        title: 'Title',
        description: 'Description',
        category: 'Category',
        duration: 'Duration (minutes)',
        startTime: 'Start date & time',
        productivity: 'Productivity (1-10)',
        save: 'Save Activity',
        recentActivities: 'Recent Activities',
        madeWith: 'Made with FastAPI + Gemini + Chart.js',
    }
};

// ===== Navigation =====
document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const view = btn.dataset.view;
        document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById(view).classList.add('active');

        // Load view data
        if (view === 'overview') loadOverview();
        else if (view === 'daily') loadDailyChart();
        else if (view === 'categories') loadCategoriesChart();
        else if (view === 'add') { loadCategories(); loadRecentActivities(); }
    });
});

// ===== Language Switcher =====
document.getElementById('languageSelector').addEventListener('change', (e) => {
    currentLang = e.target.value;
    updateLanguage();
});

function updateLanguage() {
    const t = i18n[currentLang];
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.dataset.i18n;
        if (t[key]) el.textContent = t[key];
    });
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.dataset.i18nPlaceholder;
        if (t[key]) el.placeholder = t[key];
    });
}

// ===== API Calls =====

async function apiGet(endpoint) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        return null;
    }
}

async function apiPost(endpoint, data) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || `HTTP ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// ===== Load Overview =====
async function loadOverview() {
    const summary = await apiGet('/analytics/summary?days=30');
    if (summary) {
        document.getElementById('totalActivities').textContent = summary.total_activities || 0;
        document.getElementById('totalHours').textContent = (summary.total_hours || 0).toFixed(1) + 'h';
        document.getElementById('avgScore').textContent = (summary.average_productivity || 0).toFixed(1) + '/10';
        document.getElementById('bestDay').textContent = summary.most_productive_day?.date?.split('-').reverse().join('/') || '-';
    }
}

// ===== AI Insights =====
document.getElementById('generateInsightsBtn').addEventListener('click', async () => {
    const btn = document.getElementById('generateInsightsBtn');
    const content = document.getElementById('aiInsightsContent');

    btn.disabled = true;
    btn.innerHTML = '<span class="loading"></span> Analizando...';
    content.innerHTML = '<p class="placeholder">🤖 Analizando tus datos con IA...</p>';

    try {
        const result = await apiPost('/chat/insights', { days: 30 });
        if (result && result.insights) {
            content.innerHTML = `<div style="white-space: pre-wrap;">${result.insights}</div>`;
        }
    } catch (error) {
        content.innerHTML = `<p style="color: #EF4444;">❌ Error: ${error.message}</p>`;
    } finally {
        btn.disabled = false;
        btn.innerHTML = `<span data-i18n="generate">${i18n[currentLang].generate}</span>`;
    }
});

// ===== Daily Chart =====
async function loadDailyChart() {
    const data = await apiGet('/analytics/daily?days=7');
    if (!data) return;

    const ctx = document.getElementById('dailyChart');
    if (dailyChart) dailyChart.destroy();

    dailyChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => {
                const date = new Date(d.date);
                return date.toLocaleDateString('es-ES', { weekday: 'short', day: 'numeric' });
            }),
            datasets: [{
                label: 'Horas trabajadas',
                data: data.map(d => d.hours),
                backgroundColor: '#10366D',
                borderRadius: 8,
            }, {
                label: 'Productividad (x10)',
                data: data.map(d => d.avg_score * 10),
                backgroundColor: '#2C8C57',
                borderRadius: 8,
                yAxisID: 'y1',
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'top' } },
            scales: {
                y: { beginAtZero: true, title: { display: true, text: 'Horas' } },
                y1: { beginAtZero: true, position: 'right', title: { display: true, text: 'Score' }, grid: { drawOnChartArea: false } },
            },
        },
    });
}

// ===== Categories Chart =====
async function loadCategoriesChart() {
    const data = await apiGet('/analytics/by-category?days=30');
    if (!data) return;

    const ctx = document.getElementById('categoriesChart');
    if (categoriesChart) categoriesChart.destroy();

    categoriesChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.map(c => `${c.icon || ''} ${c.name}`),
            datasets: [{
                data: data.map(c => c.total_hours),
                backgroundColor: data.map(c => c.color),
                borderWidth: 2,
                borderColor: '#fff',
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'right' },
                tooltip: {
                    callbacks: {
                        label: (context) => `${context.label}: ${context.parsed}h`,
                    },
                },
            },
        },
    });

    // Render list
    const list = document.getElementById('categoriesList');
    list.innerHTML = data.map(c => `
        <div class="category-item" style="border-left-color: ${c.color}">
            <div class="category-info">
                <span class="category-icon">${c.icon || '📌'}</span>
                <div>
                    <div class="category-name">${c.name}</div>
                    <div style="font-size: 13px; color: var(--text-muted);">${c.activity_count} actividades</div>
                </div>
            </div>
            <div class="category-stats">
                <div><strong>${c.total_hours.toFixed(1)}h</strong></div>
                <div>⭐ ${(c.average_productivity || 0).toFixed(1)}/10</div>
            </div>
        </div>
    `).join('');
}

// ===== Chat =====
document.getElementById('chatSendBtn').addEventListener('click', sendChatMessage);
document.getElementById('chatInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendChatMessage();
});

async function sendChatMessage() {
    const input = document.getElementById('chatInput');
    const question = input.value.trim();
    if (!question) return;

    addChatMessage(question, 'user');
    input.value = '';

    // Show loading
    const loadingId = addChatMessage('...', 'bot', true);

    try {
        const result = await apiPost('/chat/ask', { question, days: 30 });
        document.getElementById(loadingId).remove();
        if (result && result.answer) {
            addChatMessage(result.answer, 'bot');
        }
    } catch (error) {
        document.getElementById(loadingId).remove();
        addChatMessage(`❌ Error: ${error.message}`, 'bot');
    }
}

function addChatMessage(text, sender, isLoading = false) {
    const messagesDiv = document.getElementById('chatMessages');
    const msgId = `msg-${Date.now()}-${Math.random()}`;
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${sender}`;
    messageDiv.id = msgId;
    messageDiv.innerHTML = `
        <div class="message-avatar">${sender === 'user' ? '👤' : '🤖'}</div>
        <div class="message-content">${isLoading ? '<span class="loading"></span> Pensando...' : text}</div>
    `;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    return msgId;
}

// ===== Add Activity Form =====
async function loadCategories() {
    const categories = await apiGet('/activities/categories/all');
    const select = document.getElementById('category');
    if (categories) {
        select.innerHTML = categories.map(c =>
            `<option value="${c.id}">${c.icon || ''} ${c.name}</option>`
        ).join('');
    }
}

document.getElementById('activityForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = {
        title: document.getElementById('title').value,
        description: document.getElementById('description').value || null,
        category_id: parseInt(document.getElementById('category').value),
        duration_minutes: parseFloat(document.getElementById('duration').value),
        start_time: new Date(document.getElementById('startTime').value).toISOString(),
        productivity_score: parseInt(document.getElementById('productivity').value) || null,
    };

    try {
        await apiPost('/activities/', formData);
        alert('✅ Actividad guardada');
        e.target.reset();
        loadRecentActivities();
    } catch (error) {
        alert(`❌ Error: ${error.message}`);
    }
});

// Set default datetime to now
document.getElementById('startTime').value = new Date().toISOString().slice(0, 16);

// ===== Recent Activities =====
async function loadRecentActivities() {
    const activities = await apiGet('/activities/?limit=10');
    const list = document.getElementById('activitiesList');
    if (activities && activities.length > 0) {
        list.innerHTML = activities.map(a => `
            <div class="activity-item">
                <div class="activity-item-info">
                    <div class="activity-item-title">${a.title}</div>
                    <div class="activity-item-meta">
                        ${a.category_icon || '📌'} ${a.category_name || 'Sin categoría'}
                        · ${new Date(a.start_time).toLocaleDateString('es-ES')}
                    </div>
                </div>
                <div class="activity-item-duration">${(a.duration_minutes / 60).toFixed(1)}h</div>
            </div>
        `).join('');
    } else {
        list.innerHTML = '<p style="text-align:center; color:var(--text-muted); padding:20px;">No hay actividades aún</p>';
    }
}

// ===== Initialize =====
loadOverview();
updateLanguage();