document.addEventListener('DOMContentLoaded', () => {
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    const previewContainer = document.getElementById('preview-container');
    const processBtn = document.getElementById('process-btn');
    const toolSelect = document.getElementById('tool-select');

    // Pegar ferramenta da URL se existir
    const urlParams = new URLSearchParams(window.location.search);
    const toolId = urlParams.get('tool');
    if (toolId && toolSelect) {
        toolSelect.value = toolId;
    }

    if (uploadArea) {
        uploadArea.addEventListener('click', () => fileInput.click());

        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleFile(files[0]);
            }
        });

        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFile(e.target.files[0]);
            }
        });
    }

    function handleFile(file) {
        // Validação básica
        const allowedTypes = ['image/png', 'image/jpeg', 'image/webp', 'audio/mpeg', 'audio/wav'];
        if (!allowedTypes.includes(file.type)) {
            api.notify('Tipo de arquivo não suportado.', 'error');
            return;
        }

        // Preview se for imagem
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = (e) => {
                previewContainer.innerHTML = `<img src="${e.target.result}" style="max-width: 100%; border-radius: 8px; margin-top: 1rem;">`;
            };
            reader.readAsDataURL(file);
        } else {
            previewContainer.innerHTML = `<div style="margin-top: 1rem;">📄 ${file.name}</div>`;
        }

        processBtn.disabled = false;
        window.selectedFile = file;
    }

    if (processBtn) {
        processBtn.addEventListener('click', async () => {
            if (!window.selectedFile) return;

            const formData = new FormData();
            formData.append('file', window.selectedFile);
            formData.append('tool', toolSelect.value);

            try {
                processBtn.disabled = true;
                processBtn.innerText = 'Processando...';
                
                const response = await api.uploadFile('/process/', formData);
                
                if (response && response.task_id) {
                    pollStatus(response.task_id);
                }
            } catch (error) {
                processBtn.disabled = false;
                processBtn.innerText = 'Iniciar Processamento';
            }
        });
    }

    async function pollStatus(taskId) {
        const progressBar = document.getElementById('progress-bar');
        const progressContainer = document.getElementById('progress-container');
        
        progressContainer.style.display = 'block';
        
        const interval = setInterval(async () => {
            try {
                const status = await api.fetchAPI(`/process/status/${taskId}`);
                
                if (status.progress) {
                    progressBar.style.width = `${status.progress}%`;
                }

                if (status.status === 'completed') {
                    clearInterval(interval);
                    api.notify('Processamento concluído!', 'success');
                    setTimeout(() => {
                        window.location.href = 'history.html';
                    }, 1500);
                } else if (status.status === 'failed') {
                    clearInterval(interval);
                    api.notify('Falha no processamento.', 'error');
                    processBtn.disabled = false;
                }
            } catch (error) {
                clearInterval(interval);
            }
        }, 2000);
    }
});
