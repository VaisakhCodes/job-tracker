const API_BASE = 'http://127.0.0.1:8000';

function getToken() {
    return localStorage.getItem('token');
}

function setToken(token) {
    localStorage.setItem('token', token);
}

function clearToken() {
    localStorage.removeItem('token');
}

function authHeaders() {
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getToken()}`
    };
}

// Redirect to login if not authenticated
function requireAuth() {
    if (!getToken()) {
        window.location.href = 'login.html';
    }
}

const api = {
    async register(email, fullName, password) {
        const res = await fetch(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, full_name: fullName, password })
        });
        return res.json();
    },

    async login(email, password) {
        const res = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `username=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`
        });
        return res.json();
    },

    async getApplications(status = null) {
        const url = status
            ? `${API_BASE}/applications/?status=${status}`
            : `${API_BASE}/applications/`;
        const res = await fetch(url, { headers: authHeaders() });
        return res.json();
    },

    async createApplication(data) {
        const res = await fetch(`${API_BASE}/applications/`, {
            method: 'POST',
            headers: authHeaders(),
            body: JSON.stringify(data)
        });
        return res.json();
    },

    async updateApplication(id, data) {
        const res = await fetch(`${API_BASE}/applications/${id}`, {
            method: 'PATCH',
            headers: authHeaders(),
            body: JSON.stringify(data)
        });
        return res.json();
    },

    async deleteApplication(id) {
        await fetch(`${API_BASE}/applications/${id}`, {
            method: 'DELETE',
            headers: authHeaders()
        });
    },

    async analyse(jobDescription, resumeText, applicationId = null) {
        const res = await fetch(`${API_BASE}/analyse/`, {
            method: 'POST',
            headers: authHeaders(),
            body: JSON.stringify({
                job_description: jobDescription,
                resume_text: resumeText,
                application_id: applicationId
            })
        });
        return res.json();
    }
};