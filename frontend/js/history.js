document.addEventListener('DOMContentLoaded', async () => {
    const historyTable = document.getElementById('history-table-body');

    if (historyTable) {
        try {
            const history = await api.fetchAPI('/history/');
            
            if (history && history.length > 0) {
                historyTable.innerHTML = history.map(item => `
                    <tr>
                        <td>${item.tool_name}</td>
                        <td>${new Date(item.created_at).toLocaleDateString()}</td>
                        <td><span class="status-badge status-${item.status}">${item.status}</span></td>
                        <td>
                            ${item.status === 'completed' ? 
                                `<a href="${item.download_url}" class="btn btn-outline" style="padding: 0.25rem 0.5rem; font-size: 0.8rem;">Download</a>` : 
                                '-'}
                        </td>
                    </tr>
                `).join('');
            } else {
                historyTable.innerHTML = '<tr><td colspan="4" style="text-align: center; padding: 2rem;">Nenhum histórico encontrado.</td></tr>';
            }
        } catch (error) {
            console.error('Erro ao carregar histórico:', error);
        }
    }
});
