const API_BASE_URL = 'http://127.0.0.1:8000/api/processing/';

const processing = {
    async processImage(action, file, format = 'PNG') {
        const token = localStorage.getItem('access_token');
        if (!token) {
            return { success: false, error: 'Usuário não autenticado' };
        }

        const formData = new FormData();
        formData.append('file', file);
        if (action === 'convert') {
            formData.append('format', format);
        }

        try {
            const response = await fetch(`${API_BASE_URL}image/${action}/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData
            });
            const data = await response.json();
            if (response.ok) {
                return { success: true, result_url: data.result_url };
            }
            return { success: false, error: data.error || 'Erro no processamento' };
        } catch (error) {
            return { success: false, error: 'Erro de conexão' };
        }
    },

    async processAudio(action, file, format = 'MP3') {
        const token = localStorage.getItem('access_token');
        if (!token) {
            return { success: false, error: 'Usuário não autenticado' };
        }

        const formData = new FormData();
        formData.append('file', file);
        formData.append('format', format);

        try {
            const response = await fetch(`${API_BASE_URL}audio/${action}/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData
            });
            const data = await response.json();
            if (response.ok) {
                return { success: true, result_url: data.result_url };
            }
            return { success: false, error: data.error || 'Erro no processamento' };
        } catch (error) {
            return { success: false, error: 'Erro de conexão' };
        }
    }
};

export default processing;
