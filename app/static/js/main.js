// Global functions for NucleoTech

async function checkAuth() {
    try {
        const response = await fetch('/api/current_user');
        if (response.ok) {
            const user = await response.json();
            updateNavbar(user);
            return user;
        } else {
            updateNavbar(null);
            return null;
        }
    } catch (error) {
        console.error('Erro ao verificar autenticação:', error);
        updateNavbar(null);
        return null;
    }
}

function updateNavbar(user) {
    const authButtons = document.getElementById('auth-buttons');
    if (!authButtons) return;

    if (user) {
        let adminLink = user.is_admin ? `<li><a href="/admin">Painel Admin</a></li>` : '';
        authButtons.innerHTML = `
            <ul style="display: flex; gap: 1.5rem; align-items: center;">
                ${adminLink}
                <li><a href="/perfil">Olá, ${user.username}</a></li>
                <li><button onclick="logout()" class="btn btn-outline">Sair</button></li>
            </ul>
        `;
    } else {
        authButtons.innerHTML = `
            <a href="/login" class="btn btn-outline">Login</a>
            <a href="/cadastro" class="btn btn-primary">Cadastrar</a>
        `;
    }
}

async function logout() {
    try {
        const response = await fetch('/api/logout');
        if (response.ok) {
            window.location.href = '/';
        }
    } catch (error) {
        console.error('Erro ao fazer logout:', error);
    }
}

// Format currency
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.padding = '1rem 2rem';
    notification.style.borderRadius = '4px';
    notification.style.color = '#fff';
    notification.style.backgroundColor = type === 'success' ? '#28a745' : '#dc3545';
    notification.style.zIndex = '2000';
    notification.innerText = message;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Initialize auth check on all pages
document.addEventListener('DOMContentLoaded', checkAuth);
