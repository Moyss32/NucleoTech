const API_BASE_URL = 'http://127.0.0.1:8000/api'; // Base URL com prefixo /api

const api = {
    async fetchAPI(endpoint, method = 'GET', data = null) {
        const token = localStorage.getItem('access_token');
        
        const headers = {
            'Content-Type': 'application/json',
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const config = {
            method,
            headers,
        };

       if (data && method !== 'GET') {
        config.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
            
            if (response.status === 401) {
                // Token expirado ou inválido
                this.logout();
                return null;
            }

            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.message || 'Erro na requisição');
            }

            return result;
        } catch (error) {
            console.error('API Error:', error);
            this.notify(error.message, 'error');
            throw error;
        }
    },

    async uploadFile(endpoint, formData) {
        const token = localStorage.getItem('access_token');
        const headers = {};

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'POST',
                headers,
                body: formData
            });

            if (response.status === 401) {
                this.logout();
                return null;
            }

            const result = await response.json();
            if (!response.ok) throw new Error(result.message || 'Erro no upload');
            return result;
        } catch (error) {
            this.notify(error.message, 'error');
            throw error;
        }
    },

    logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/pages/login.html';
    },

    notify(message, type = 'info') {
        const container = document.getElementById('notification-container');
        if (!container) {
            const div = document.createElement('div');
            div.id = 'notification-container';
            document.body.appendChild(div);
        }
        
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerText = message;
        
        document.getElementById('notification-container').appendChild(notification);
        
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
};

// Exportar para uso global se não estiver usando módulos, 
// mas como é MPA simples, vamos deixar no escopo global ou usar export se necessário.
window.api = api;
