/* Centralized REST API Client & Health Monitor */
const getBackendOrigin = () => {
  if (window.ENV_API_URL && window.ENV_API_URL.trim() !== '') {
    return window.ENV_API_URL.replace(/\/$/, '');
  }
  const origin = window.location.origin;
  if (origin.includes('localhost:8000') || origin.includes('127.0.0.1:8000')) {
    return '';
  }
  if (origin.includes('localhost') || origin.includes('127.0.0.1')) {
    return 'http://localhost:8000';
  }
  return 'https://enterprise-rag-backend-3qpl.onrender.com';
};

const SERVER_ORIGIN = getBackendOrigin();
const API_BASE_URL = `${SERVER_ORIGIN}/api/v1`;

async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem('token');
  const headers = options.headers || {};

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  if (!(options.body instanceof FormData) && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json';
  }

  const config = {
    ...options,
    headers,
  };

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

    if (response.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      if (!window.location.pathname.endsWith('login.html') && !window.location.pathname.endsWith('register.html')) {
        window.location.href = 'login.html';
      }
      throw new Error('Invalid email or password.');
    }

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      const message = errorData.detail || errorData.message || (
        response.status === 503 ? 'Database service is temporarily unavailable.' :
        response.status === 500 ? 'An unexpected server error occurred.' :
        `Server Error (${response.status})`
      );
      throw new Error(message);
    }

    if (response.status === 204) {
      return null;
    }

    return await response.json();
  } catch (err) {
    console.error(`API Error [${endpoint}]:`, err);
    if (err.name === 'TypeError' || err.message.includes('fetch')) {
      throw new Error('Unable to reach the AI service. Please try again.');
    }
    throw err;
  }
}

async function checkSystemHealth() {
  try {
    const response = await fetch(`${SERVER_ORIGIN}/api/health`);
    if (response.ok) {
      const data = await response.json();
      return data.status === 'healthy';
    }
    return false;
  } catch (err) {
    return false;
  }
}

async function updateSystemStatusUI() {
  const statusEl = document.getElementById('system-status-indicator');
  if (!statusEl) return;

  const isHealthy = await checkSystemHealth();
  if (isHealthy) {
    statusEl.innerHTML = '🟢 System Operational';
    statusEl.className = 'status-indicator status-operational';
  } else {
    statusEl.innerHTML = '🔴 Backend Unavailable';
    statusEl.className = 'status-indicator status-unavailable';
  }
}

document.addEventListener('DOMContentLoaded', () => {
  updateSystemStatusUI();
  // Check health status every 60 seconds
  setInterval(updateSystemStatusUI, 60000);
});

