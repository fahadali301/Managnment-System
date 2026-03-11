/**
 * Management System - Main JavaScript
 * Handles JWT authentication, API calls, and UI interactions
 */

const API_BASE = '/api';
const TOKEN_KEY = 'ms_access_token';
const REFRESH_KEY = 'ms_refresh_token';

/* ========================
   Token Helpers
   ======================== */

function getAccessToken() {
    return localStorage.getItem(TOKEN_KEY);
}

function getRefreshToken() {
    return localStorage.getItem(REFRESH_KEY);
}

function saveTokens(access, refresh) {
    localStorage.setItem(TOKEN_KEY, access);
    if (refresh) {
        localStorage.setItem(REFRESH_KEY, refresh);
    }
}

function clearTokens() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_KEY);
}

function isAuthenticated() {
    return !!getAccessToken();
}

/* ========================
   API Fetch Wrapper
   ======================== */

async function apiFetch(endpoint, options = {}) {
    const token = getAccessToken();
    const defaultHeaders = {
        'Content-Type': 'application/json',
    };
    if (token) {
        defaultHeaders['Authorization'] = `Bearer ${token}`;
    }

    const config = {
        ...options,
        headers: {
            ...defaultHeaders,
            ...options.headers,
        },
    };

    let response = await fetch(`${API_BASE}${endpoint}`, config);

    // Attempt token refresh on 401
    if (response.status === 401 && getRefreshToken()) {
        const refreshed = await refreshAccessToken();
        if (refreshed) {
            config.headers['Authorization'] = `Bearer ${getAccessToken()}`;
            response = await fetch(`${API_BASE}${endpoint}`, config);
        } else {
            redirectToLogin();
            return null;
        }
    }

    return response;
}

async function refreshAccessToken() {
    try {
        const resp = await fetch(`${API_BASE}/token/refresh/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh: getRefreshToken() }),
        });
        if (resp.ok) {
            const data = await resp.json();
            localStorage.setItem(TOKEN_KEY, data.access);
            return true;
        }
    } catch (e) {
        console.error('Token refresh error:', e);
    }
    clearTokens();
    return false;
}

/* ========================
   Navigation Helpers
   ======================== */

function redirectToLogin() {
    clearTokens();
    window.location.href = '/login/';
}

function requireAuth() {
    if (!isAuthenticated()) {
        redirectToLogin();
    }
}

/* ========================
   Show Alert Messages
   ======================== */

function showAlert(message, type = 'info', containerId = 'alert-container') {
    const container = document.getElementById(containerId);
    if (!container) return;

    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${escapeHtml(message)}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>`;
    container.innerHTML = alertHtml;
    container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/* ========================
   Login Form Handler
   ======================== */

function initLoginForm() {
    const form = document.getElementById('loginForm');
    if (!form) return;

    // Redirect if already logged in
    if (isAuthenticated()) {
        window.location.href = '/dashboard/';
        return;
    }

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        const btn = form.querySelector('[type="submit"]');
        const originalText = btn.innerHTML;
        btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Signing in...';
        btn.disabled = true;

        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value;

        try {
            const resp = await fetch(`${API_BASE}/token/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });

            const data = await resp.json();

            if (resp.ok) {
                saveTokens(data.access, data.refresh);
                showAlert('Login successful! Redirecting…', 'success');
                setTimeout(() => { window.location.href = '/dashboard/'; }, 800);
            } else {
                const msg = data.detail || (data.non_field_errors && data.non_field_errors[0]) || 'Invalid credentials. Please try again.';
                showAlert(msg, 'danger');
            }
        } catch (err) {
            showAlert('Network error. Please check if the server is running.', 'danger');
            console.error(err);
        } finally {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    });
}

/* ========================
   Register Form Handler
   ======================== */

function initRegisterForm() {
    const form = document.getElementById('registerForm');
    if (!form) return;

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        const btn = form.querySelector('[type="submit"]');
        const originalText = btn.innerHTML;
        btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Creating account...';
        btn.disabled = true;

        const password = document.getElementById('password').value;
        const password2 = document.getElementById('password2').value;

        if (password !== password2) {
            showAlert('Passwords do not match.', 'danger');
            btn.innerHTML = originalText;
            btn.disabled = false;
            return;
        }

        const payload = {
            username: document.getElementById('username').value.trim(),
            email: document.getElementById('email').value.trim(),
            password,
            first_name: document.getElementById('first_name') ? document.getElementById('first_name').value.trim() : '',
            last_name: document.getElementById('last_name') ? document.getElementById('last_name').value.trim() : '',
        };

        try {
            const resp = await fetch(`${API_BASE}/users/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });

            if (resp.ok) {
                showAlert('Account created! Redirecting to login…', 'success');
                setTimeout(() => { window.location.href = '/login/'; }, 1200);
            } else {
                const data = await resp.json();
                const msg = Object.values(data).flat().join(' ');
                showAlert(msg || 'Registration failed. Please try again.', 'danger');
            }
        } catch (err) {
            showAlert('Network error. Please try again.', 'danger');
            console.error(err);
        } finally {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    });
}

/* ========================
   Dashboard Loader
   ======================== */

async function loadDashboardStats() {
    requireAuth();

    const setCount = (id, value) => {
        const el = document.getElementById(id);
        if (el) el.textContent = value;
    };

    try {
        const [companiesResp, branchesResp, usersResp, assetsResp] = await Promise.all([
            apiFetch('/companies/'),
            apiFetch('/branches/'),
            apiFetch('/users/'),
            apiFetch('/assets/'),
        ]);

        if (companiesResp && companiesResp.ok) {
            const data = await companiesResp.json();
            setCount('stat-companies', Array.isArray(data) ? data.length : (data.count || 0));
            renderRecentCompanies(Array.isArray(data) ? data.slice(0, 5) : []);
        }
        if (branchesResp && branchesResp.ok) {
            const data = await branchesResp.json();
            setCount('stat-branches', Array.isArray(data) ? data.length : (data.count || 0));
        }
        if (usersResp && usersResp.ok) {
            const data = await usersResp.json();
            setCount('stat-users', Array.isArray(data) ? data.length : (data.count || 0));
        }
        if (assetsResp && assetsResp.ok) {
            const data = await assetsResp.json();
            setCount('stat-assets', Array.isArray(data) ? data.length : (data.count || 0));
        }
    } catch (err) {
        console.error('Dashboard load error:', err);
    }
}

function renderRecentCompanies(companies) {
    const tbody = document.getElementById('recent-companies-body');
    const empty = document.getElementById('companies-empty');
    if (!tbody) return;

    if (!companies || companies.length === 0) {
        tbody.closest('table').style.display = 'none';
        if (empty) empty.style.display = 'block';
        return;
    }

    tbody.innerHTML = companies.map(c => `
        <tr>
            <td><strong>${escapeHtml(c.name)}</strong></td>
            <td>${escapeHtml(c.address || '—')}</td>
            <td>${escapeHtml(c.city || '—')}</td>
            <td><span class="badge bg-success">Active</span></td>
            <td>
                <a href="/companies/" class="btn btn-sm btn-outline-primary">View</a>
            </td>
        </tr>`).join('');
}

/* ========================
   Companies List Loader
   ======================== */

async function loadCompanies() {
    requireAuth();
    const tbody = document.getElementById('companies-tbody');
    const empty = document.getElementById('companies-empty');
    if (!tbody) return;

    try {
        const resp = await apiFetch('/companies/');
        if (!resp || !resp.ok) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center text-danger">Failed to load companies.</td></tr>';
            return;
        }
        const data = await resp.json();
        const companies = Array.isArray(data) ? data : (data.results || []);

        if (companies.length === 0) {
            tbody.closest('table').style.display = 'none';
            if (empty) empty.style.display = 'block';
            return;
        }

        tbody.innerHTML = companies.map(c => `
            <tr>
                <td>${c.id}</td>
                <td><strong>${escapeHtml(c.name)}</strong></td>
                <td>${escapeHtml(c.address || '—')}</td>
                <td>${escapeHtml(c.city || '—')}</td>
                <td>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteCompany(${c.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>`).join('');
    } catch (err) {
        console.error('Load companies error:', err);
        tbody.innerHTML = '<tr><td colspan="5" class="text-center text-danger">Error loading data.</td></tr>';
    }
}

async function deleteCompany(id) {
    if (!confirm('Are you sure you want to delete this company?')) return;
    const resp = await apiFetch(`/companies/${id}/`, { method: 'DELETE' });
    if (resp && (resp.ok || resp.status === 204)) {
        showAlert('Company deleted successfully.', 'success');
        loadCompanies();
    } else {
        showAlert('Failed to delete company.', 'danger');
    }
}

/* ========================
   Employees List Loader
   ======================== */

async function loadEmployees() {
    requireAuth();
    const tbody = document.getElementById('employees-tbody');
    const empty = document.getElementById('employees-empty');
    if (!tbody) return;

    try {
        const resp = await apiFetch('/users/');
        if (!resp || !resp.ok) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center text-danger">Failed to load employees.</td></tr>';
            return;
        }
        const data = await resp.json();
        const users = Array.isArray(data) ? data : (data.results || []);

        if (users.length === 0) {
            tbody.closest('table').style.display = 'none';
            if (empty) empty.style.display = 'block';
            return;
        }

        tbody.innerHTML = users.map(u => `
            <tr>
                <td>${u.id}</td>
                <td><strong>${escapeHtml(u.username)}</strong></td>
                <td>${escapeHtml((u.first_name || '') + ' ' + (u.last_name || '')).trim() || '—'}</td>
                <td>${escapeHtml(u.email || '—')}</td>
                <td>${escapeHtml(u.address || '—')}</td>
            </tr>`).join('');
    } catch (err) {
        console.error('Load employees error:', err);
        tbody.innerHTML = '<tr><td colspan="5" class="text-center text-danger">Error loading data.</td></tr>';
    }
}

/* ========================
   Logout Handler
   ======================== */

function initLogout() {
    const logoutLinks = document.querySelectorAll('.logout-link');
    logoutLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            clearTokens();
            window.location.href = '/login/';
        });
    });
}

/* ========================
   Highlight Active Nav
   ======================== */

function highlightActiveNav() {
    const path = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === path) {
            link.classList.add('active');
        }
    });
}

/* ========================
   Auto-dismiss Alerts
   ======================== */

function initAutoDismissAlerts() {
    document.querySelectorAll('.alert[data-auto-dismiss]').forEach(alert => {
        const delay = parseInt(alert.dataset.autoDismiss, 10) || 4000;
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, delay);
    });
}

/* ========================
   Init on DOM Ready
   ======================== */

document.addEventListener('DOMContentLoaded', function () {
    initLoginForm();
    initRegisterForm();
    initLogout();
    highlightActiveNav();
    initAutoDismissAlerts();

    // Page-specific initializers
    if (document.getElementById('dashboard-page')) {
        loadDashboardStats();
    }
    if (document.getElementById('companies-page')) {
        loadCompanies();
    }
    if (document.getElementById('employees-page')) {
        loadEmployees();
    }
});
