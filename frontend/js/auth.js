document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(loginForm);
            const data = Object.fromEntries(formData.entries());

            try {
                const response = await api.fetchAPI('/auth/login/', 'POST', data);
                if (response && response.access) {
                    localStorage.setItem('access_token', response.access);
                    localStorage.setItem('refresh_token', response.refresh);
                    api.notify('Login realizado com sucesso!', 'success');
                    setTimeout(() => {
                        window.location.href = 'dashboard.html';
                    }, 1000);
                }
            } catch (error) {
                // Erro já tratado no api.js
            }
        });
    }

    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(registerForm);
            const data = Object.fromEntries(formData.entries());

            try {
                const response = await api.fetchAPI('/auth/register/', 'POST', data);
                if (response) {
                    api.notify('Cadastro realizado! Faça login para continuar.', 'success');
                    setTimeout(() => {
                        window.location.href = 'login.html';
                    }, 2000);
                }
            } catch (error) {
                // Erro já tratado
            }
        });
    }
});
