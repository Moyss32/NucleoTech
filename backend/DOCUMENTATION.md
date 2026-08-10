# Documentação Técnica: FileProcessor Pro Backend

Esta documentação detalha a arquitetura, configuração e utilização do backend do **FileProcessor Pro**, uma plataforma robusta para processamento de arquivos (imagens e áudio) utilizando inteligência artificial e processamento assíncrono.

---

## 1. Visão Geral da Arquitetura

O sistema foi construído seguindo princípios de escalabilidade e desacoplamento, utilizando as seguintes tecnologias:

- **Framework:** Django 5.x / Django REST Framework

- **Processamento Assíncrono:** Celery + Redis

- **Banco de Dados:** SQLite (Desenvolvimento) / PostgreSQL (Produção recomendado)

- **Processamento de Mídia:** RemBG (IA), ImageMagick (Wand), FFmpeg

- **Pagamentos:** Stripe API

### Fluxo de Processamento

1. O cliente envia um arquivo via endpoint de `/api/process/`.

1. O backend valida as permissões e limites do plano do usuário.

1. O arquivo é salvo e uma tarefa é enfileirada no **Redis**.

1. O **Celery Worker** consome a tarefa e executa a ferramenta de processamento (RemBG, FFmpeg, etc.).

1. O status é atualizado no banco de dados.

1. O cliente consulta o status via polling e baixa o resultado através de um **link seguro**.

---

## 2. Instalação e Configuração

### Requisitos de Sistema (Ubuntu/Debian)

O backend depende de bibliotecas binárias para o processamento de mídia:

```bash
sudo apt-get update
sudo apt-get install -y libmagickwand-dev ffmpeg redis-server
```

### Configuração do Ambiente Python

Recomendamos o uso de um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Variáveis de Ambiente (.env)

Crie um arquivo `.env` na raiz do projeto `django_project/`:

```
DEBUG=True
SECRET_KEY=sua_chave_secreta
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
REDIS_URL=redis://localhost:6379/0
```

---

## 3. API Reference

Todos os endpoints requerem o prefixo `/api/` e autenticação via **Bearer Token**, exceto onde indicado.

### Autenticação

| Endpoint | Método | Descrição |
| --- | --- | --- |
| `/auth/login/` | `POST` | Obtém tokens Access e Refresh. |
| `/auth/register/` | `POST` | Registra um novo usuário. |

### Processamento de Arquivos

#### Iniciar Processamento

`POST /api/process/`

- **Body (Multipart/FormData):**
  - `file`: O arquivo a ser processado.
  - `tool`: Slug da ferramenta (`remove-bg`, `convert-image`, `upscale`, `thumbnail`, `convert-audio`).

- **Resposta:** `{"task_id": "uuid", "status": "queued"}`

#### Consultar Status

`GET /api/process/status/<task_id>/`

- **Resposta:** `{"status": "completed", "progress": 100, "result_url": "..."}`

### Gerenciamento de Arquivos e Download

#### Histórico do Usuário

`GET /api/history/`

- Retorna a lista de todas as execuções e arquivos processados pelo usuário.

#### Download Seguro

`GET /api/download/<arquivo_uuid>/`

- Valida se o usuário autenticado é o dono do arquivo antes de iniciar o stream do arquivo.

---

## 4. Sistema de Planos e Assinaturas

O sistema utiliza um modelo de **Quotas Dinâmicas** baseado no plano ativo do usuário.

| Plano | Limite Mensal | Limite Diário | Tamanho Máx. | Upscale IA |
| --- | --- | --- | --- | --- |
| **Gratuito** | 10 | 2 | 5 MB | Não |
| **Pro** | 100 | 10 | 50 MB | Sim |
| **Enterprise** | 1000 | 50 | 500 MB | Sim |

### Integração Stripe

- **Checkout:** `POST /api/stripe/create-checkout-session/` cria uma sessão de pagamento.

- **Webhooks:** O endpoint `/api/stripe/webhook/` (público) processa eventos `checkout.session.completed` para ativar o plano instantaneamente.

---

## 5. Manutenção e Comandos Úteis

### Iniciar o Worker do Celery

Essencial para que o processamento de arquivos funcione:

```bash
celery -A core worker --loglevel=info
```

### Popular o Banco de Dados (Seed)

Cria os serviços e planos iniciais:

```bash
python scripts/database_seed.py
```

### Limpeza de Arquivos Temporários

Arquivos na pasta `media/uploads/` e `media/results/` devem ser limpos periodicamente via tarefa agendada (Cron) se não houver persistência em S3.

---

## 6. Considerações de Segurança

1. **UUIDs:** Todos os arquivos e execuções utilizam UUIDs para evitar ataques de enumeração.

1. **Validação de MIME:** O sistema valida o tipo real do arquivo, não apenas a extensão.

1. **Download Protegido:** Arquivos não são servidos diretamente pelo servidor web (Nginx/Apache) sem passar pela validação do Django, garantindo que apenas o dono acesse o resultado.

