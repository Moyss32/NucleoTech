/**
 * js/api.js
 * Utilitário central para chamadas à API REST do NucleoTech.
 */

const BASE_URL = 'http://localhost:8000'; // Substitua pela URL base da sua API

/**
 * Função genérica para realizar requisições à API com autenticação JWT.
 * @param {string} endpoint - Rota da API (ex: '/api/user/dashboard/')
 * @param {string} method - Método HTTP (GET, POST, etc.)
 * @param {object|FormData} data - Dados do corpo da requisição
 * @returns {Promise<object>} Resposta JSON da API
 */
export async function fetchAPI(endpoint, method = 'GET', data = null) {
    const url = `${BASE_URL}${endpoint}`;
    
    // Configura os headers básicos
    const headers = new Headers();
    
    // Se não for FormData (usado para upload de arquivos), define como JSON
    if (!(data instanceof FormData)) {
        headers.append('Content-Type', 'application/json');
    }

    // Adiciona o token JWT se o usuário estiver autenticado
    const token = localStorage.getItem('access_token');
    if (token) {
        headers.append('Authorization', `Bearer ${token}`);
    }

    const options = {
        method,
        headers,
    };

    if (data) {
        options.body = data instanceof FormData ? data : JSON.stringify(data);
    }

    try {
        const response = await fetch(url, options);

        // Se o token expirou (401), você pode implementar a lógica do refresh_token aqui futuramente
        if (response.status === 401) {
            console.warn("Token expirado ou inválido. Redirecionando para login...");
            localStorage.removeItem('access_token');
            window.location.href = '/pages/login.html';
        }

        const jsonResponse = await response.json();

        if (!response.ok) {
            throw new Error(jsonResponse.message || 'Erro na requisição da API');
        }

        return jsonResponse;
    } catch (error) {
        console.error(`Erro na API (${method} ${endpoint}):`, error);
        throw error;
    }
}