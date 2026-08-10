document.addEventListener('DOMContentLoaded', async () => {
    const dashboardStats = document.getElementById('dashboard-stats');
    const toolsGrid = document.getElementById('tools-grid');

    if (dashboardStats || toolsGrid) {
        try {
            const data = await api.fetchAPI('/user/dashboard/');
            
            if (dashboardStats && data) {
                document.getElementById('user-plan').innerText = data.plano || 'Gratuito';
                document.getElementById('usage-count').innerText = data.uso_mensal_atual || 0;
            }

            // Se estiver na página de ferramentas, carregar cards
            if (toolsGrid) {
                renderTools();
            }
        } catch (error) {
            console.error('Erro ao carregar dashboard:', error);
        }
    }
});

function renderTools() {
    const tools = [
        { id: 'remove-bg', name: 'Remover Fundo', desc: 'Remova o fundo de qualquer imagem instantaneamente.', icon: '<img src="../assets/icons/bg-remove.png" style="width: 24px;">' },
        { id: 'convert-image', name: 'Converter Imagem', desc: 'PNG, JPG, WebP e mais.', icon: '<img src="../assets/icons/img-convert.png" style="width: 24px;">' },
        { id: 'upscale', name: 'Upscale 1.5x', desc: 'Aumente a resolução sem perder qualidade.', icon: '<img src="../assets/icons/upscale.png" style="width: 24px;">' },
        { id: 'thumbnail', name: 'Gerador de Thumbnails', desc: 'Crie capas incríveis para seus vídeos.', icon: '📹' },
        { id: 'convert-audio', name: 'Conversor de Áudio', desc: 'WAV para MP3 e vice-versa.', icon: '<img src="../assets/icons/audio-convert.png" style="width: 24px;">' }
    ];

    const grid = document.getElementById('tools-grid');
    if (!grid) return;

    grid.innerHTML = tools.map(tool => `
        <div class="card" onclick="window.location.href='upload.html?tool=${tool.id}'">
            <div class="card-icon">${tool.icon}</div>
            <h3>${tool.name}</h3>
            <p>${tool.desc}</p>
            <button class="btn btn-ghost btn-sm" style="width: 100%">Usar Ferramenta</button>
        </div>
    `).join('');
}
