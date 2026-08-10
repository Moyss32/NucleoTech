document.addEventListener('DOMContentLoaded', async () => {
    const profileInfo = document.getElementById('profile-info');
    const subscriptionInfo = document.getElementById('subscription-info');

    if (profileInfo) {
        try {
            const profile = await api.fetchAPI('/user/profile/');
            if (profile) {
                document.getElementById('profile-username').innerText = profile.username;
                document.getElementById('profile-email').innerText = profile.email;
                // document.getElementById('profile-plan').innerText = profile.plan_name;
            }
        } catch (error) {}
    }

    if (subscriptionInfo) {
        try {
            const sub = await api.fetchAPI('/subscription/');
            if (sub) {
                document.getElementById('current-plan-name').innerText = sub.plano_nome;
                document.getElementById('plan-limit').innerText = `${sub.uso_atual} / ${sub.limite_mensal} execuções`;
                
                const usagePercent = (sub.uso_atual / sub.limite_mensal) * 100;
                document.getElementById('usage-progress').style.width = `${usagePercent}%`;
            }
        } catch (error) {}
    }
});
