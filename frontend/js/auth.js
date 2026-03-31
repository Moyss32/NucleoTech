const API_BASE_URL = 'http://127.0.0.1:8000/api/users/';

const auth = {
    async login(username, password) {
        try {
            const response = await fetch(`${API_BASE_URL}login/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            const data = await response.json();
            if (response.ok) {
                localStorage.setItem('access_token', data.access);
                localStorage.setItem('refresh_token', data.refresh);
                return { success: true };
            }
            return { success: false, error: data.detail || 'Erro ao fazer login' };
        } catch (error) {
            return { success: false, error: 'Erro de conexão' };
        }
    },

    async register(username, email, password) {
        try {
            const response = await fetch(`${API_BASE_URL}register/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password })
            });
            const data = await response.json();
            if (response.ok) {
                return { success: true };
            }
            return { success: false, error: data.detail || 'Erro ao cadastrar' };
        } catch (error) {
            return { success: false, error: 'Erro de conexão' };
        }
    },

    logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = 'login.html';
    },

    getToken() {
        return localStorage.getItem('access_token');
    },

    isAuthenticated() {
        return !!this.getToken();
    }
};

export default auth;
