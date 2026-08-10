# NucleoTech Backend

Backend principal do projeto NucleoTech, desenvolvido com Django + Django REST Framework.

O núcleo do sistema está concentrado em:

```txt
backend/django_project/
```

A aplicação funciona como uma API REST para autenticação, gerenciamento de usuários, assinaturas e processamento de arquivos locais.

---

# Estrutura do Projeto

```txt
backend/
├── django_project/
│   ├── api/                     # Rotas principais da API
│   ├── apps/
│   │   ├── users/              # Usuários e autenticação
│   │   ├── subscriptions/      # Sistema de assinaturas
│   │   ├── processing/         # Processamento de arquivos
│   │   └── services/           # Serviços/ferramentas disponíveis
│   ├── core/                   # Configurações centrais do Django
│   ├── media/                  # Uploads e resultados processados
│   ├── manage.py
│   └── db.sqlite3
│
├── tools/
│   ├── image_tools/            # Ferramentas de imagem
│   └── audio_tools/            # Ferramentas de áudio
│
└── scripts/
    └── database_seed.py
```

---

# Tecnologias Utilizadas

## Backend

- Python
- Django
- Django REST Framework
- SimpleJWT
- SQLite
- Threading para tarefas assíncronas locais

## Processamento

### Ferramentas de Imagem

- Remoção de fundo
- Upscale
- Conversão de imagens
- Geração de thumbnails

### Ferramentas de Áudio

- Conversão de áudio

---

# Arquitetura Geral

O backend foi dividido em apps independentes para facilitar manutenção e escalabilidade.

## Apps Principais

| App | Responsabilidade |
|---|---|
| `users` | Cadastro, login e perfil |
| `subscriptions` | Controle de planos e limites |
| `processing` | Execução e histórico de tarefas |
| `services` | Cadastro de ferramentas disponíveis |

---

# Sistema de Autenticação

A autenticação utiliza JWT através do pacote:

```txt
rest_framework_simplejwt
```

O login retorna:

- Access Token
- Refresh Token

As rotas protegidas utilizam:

```txt
Authorization: Bearer TOKEN
```

---

# Rotas da API

Arquivo principal:

```txt
backend/django_project/api/urls.py
```

Sim, existe uma API completa de cadastro, login, autenticação e gerenciamento básico de usuários.

---

# Endpoints

## Autenticação

### Cadastro

```http
POST /api/auth/register/
```

### Body

```json
{
  "username": "usuario",
  "email": "email@email.com",
  "password": "senha"
}
```

### Login

```http
POST /api/auth/login/
```

### Body

```json
{
  "username": "usuario",
  "password": "senha"
}
```

### Resposta

```json
{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token"
}
```

---

### Refresh Token

```http
POST /api/auth/refresh/
```

---

# Usuário

## Perfil

```http
GET /api/user/profile/
```

Retorna:

```json
{
  "id": 1,
  "username": "usuario",
  "email": "email@email.com"
}
```

---

## Dashboard

```http
GET /api/user/dashboard/
```

Retorna informações do plano:

```json
{
  "plano": "Premium",
  "limite": 100,
  "uso_atual": 27
}
```

---

# Sistema de Assinaturas

## Endpoint

```http
GET /api/subscription/
```

O backend possui:

- Controle de planos
- Limites mensais
- Controle de uso
- Relação usuário ↔ assinatura

A lógica de bloqueio já está implementada:

```python
if ua.plano and ua.uso_atual >= ua.plano.limite_mensal:
```

Ou seja: quando o usuário bate o limite do plano, o processamento é bloqueado automaticamente.

Simples e eficiente. Sem aquelas arquiteturas “enterprise” absurdas que precisam de 19 microsserviços para converter uma imagem. Milagre moderno.

---

# Sistema de Processamento

O app mais importante do backend.

## Endpoint Principal

```http
POST /api/process/
```

## Envio

Formato:

```txt
multipart/form-data
```

Campos:

| Campo | Tipo |
|---|---|
| `file` | Arquivo |
| `tool` | String |

---

# Ferramentas Disponíveis

| Tool Slug | Função |
|---|---|
| `remove-bg` | Remove fundo de imagens |
| `upscale` | Aumenta resolução |
| `convert-image` | Conversão de imagens |
| `thumbnail` | Cria thumbnails |
| `convert-audio` | Conversão de áudio |

---

# Execução Assíncrona

O processamento roda em threads:

```python
threading.Thread(...)
```

Isso evita bloquear a API principal.

Atualmente o projeto usa uma abordagem local simples ao invés de:

- Celery
- Redis
- RabbitMQ

O que é perfeitamente aceitável para MVP, testes e desenvolvimento local.

Inclusive, muita gente coloca fila distribuída logo no primeiro commit e transforma um CRUD em engenharia aeroespacial.

---

# Consulta de Status

## Endpoint

```http
GET /api/process/status/<task_id>/
```

## Resposta

```json
{
  "status": "completed",
  "progress": 100,
  "download_url": "http://localhost/media/results/..."
}
```

Status possíveis:

| Status | Significado |
|---|---|
| `pending` | Na fila |
| `processing` | Em execução |
| `completed` | Finalizado |
| `failed` | Erro |

---

# Histórico

## Endpoint

```http
GET /api/history/
```

Lista todas as execuções do usuário autenticado.

---

# Banco de Dados

Atualmente:

```txt
SQLite
```

Configuração localizada em:

```txt
core/settings.py
```

Pode ser facilmente migrado para:

- PostgreSQL
- MariaDB
- MySQL

---

# Modelos Principais

## ExecucaoLocal

Representa uma tarefa de processamento.

Campos importantes:

- task_id
- status
- progresso
- data_inicio
- data_fim

---

## ArquivoProcessado

Armazena:

- Arquivo original
- Nome do arquivo
- Tamanho

---

## ResultadoProcessamento

Relaciona:

- Arquivo original
- Arquivo final processado

---

## UsoServico

Registra:

- Usuário
- Serviço utilizado
- Data
- Sucesso/Falha

---

# Armazenamento de Arquivos

Arquivos enviados:

```txt
media/uploads/
```

Resultados:

```txt
media/results/
```

---

# Configurações Importantes

## CORS

```python
CORS_ALLOW_ALL_ORIGINS = True
```

Bom para desenvolvimento.

Péssima ideia em produção sem controle adequado.

---

## JWT

```python
ACCESS_TOKEN_LIFETIME = 60 minutos
REFRESH_TOKEN_LIFETIME = 1 dia
```

---

# Como Rodar o Projeto

*É nessessario apenas rodar o arquivo .bat*
---

# Possíveis Melhorias

## Infraestrutura

- Migrar SQLite → PostgreSQL
- Implementar Celery + Redis
- Dockerização
- Rate limiting
- Logs estruturados
- Monitoramento

## Segurança

- Limitar uploads
- Validar MIME types
- Melhorar CORS
- Rate limit por IP
- Antivírus para uploads

## Performance

- Processamento distribuído
- Cache
- Compressão de arquivos
- Workers dedicados

---

# Pontos Fortes do Projeto

- Estrutura modular
- API limpa
- JWT funcionando
- Processamento desacoplado
- Organização boa para expansão
- Fácil manutenção
- Separação correta entre apps

O backend está surpreendentemente bem organizado para um projeto acadêmico/pessoal.

A divisão entre:

- autenticação
- assinatura
- serviços
- processamento

foi feita do jeito certo.

Tem vários projetos por aí que viram um monolito caótico com tudo dentro de `views.py` em duas semanas.

---

# Considerações Finais

O projeto já possui:

- API REST funcional
- Cadastro/login JWT
- Controle de usuários
- Controle de assinaturas
- Processamento assíncrono
- Histórico de execuções
- Upload e geração de arquivos

Ou seja:

O “suco” do backend realmente está dentro de:

```txt
backend/django_project/
```

principalmente em:

```txt
apps/processing/
```

que é onde toda a lógica pesada acontece.

