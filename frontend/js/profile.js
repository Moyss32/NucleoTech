document.addEventListener('DOMContentLoaded', async () => {
    const profileInfo = document.getElementById('profile-info');
    const subscriptionInfo = document.getElementById('subscription-info');

    if (profileInfo) {
        try {
            const profile = await api.fetchAPI('/user/profile/');
            if (profile) {
                document.getElementById('profile-username').innerText = profile.username;
                document.getElementById('profile-email').innerText = profile.email;
                document.getElementById('profile-plan').innerText = profile.plan_name;
            }
        } catch (error) {}
    }

    if (subscriptionInfo) {
        try {
            const sub = await api.fetchAPI('/subscription/');
            if (sub) {
                document.getElementById('current-plan-name').innerText = sub.plan_name;
                document.getElementById('plan-limit').innerText = `${sub.used_count} / ${sub.limit_count} execuções`;
                
                const usagePercent = (sub.used_count / sub.limit_count) * 100;
                document.getElementById('usage-progress').style.width = `${usagePercent}%`;
            }
        } catch (error) {}
    }
});
