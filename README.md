
##NucleoTech

descrção

## Como Configurar e Rodar o Projeto Completo

### Pré-requisitos

- Python 3.11
- MySQL Server
- `ffmpeg` (para processamento de áudio)

### Passos de Configuração

1.  **Clone o repositório e descompacte o arquivo.**

2.  **Navegue até o diretório do projeto**:
    ```bash
    cd nucleotech
    ```

3.  **Crie e ative o ambiente virtual**:
    ```bash
    python3.11 -m venv venv
    source venv/bin/activate
    ```

4.  **Instale as dependências do Python**:
    ```bash
    pip install Django mysqlclient djangorestframework djangorestframework-simplejwt Pillow rembg pydub
    ```
    *Se houver erros na instalação do `mysqlclient` ou `rembg`, certifique-se de que os pacotes de desenvolvimento do MySQL, Python e `build-essential` estejam instalados:*
    ```bash
    sudo apt-get update
    sudo apt-get install -y libmysqlclient-dev pkg-config build-essential python3.11-dev ffmpeg
    pip install mysqlclient rembg
    ```

5.  **Configure o Banco de Dados MySQL**:
    - Certifique-se de que o serviço MySQL esteja em execução.
    - Conecte-se ao MySQL como `root` (ou um usuário com privilégios administrativos) e crie o banco de dados e o usuário:
    ```bash
    sudo mysql -u root -p
    # Digite a senha do root do MySQL quando solicitado
    CREATE DATABASE IF NOT EXISTS nucleotech_db;
    CREATE USER 'nucleotech_user'@'localhost' IDENTIFIED BY 'password';
    GRANT ALL PRIVILEGES ON nucleotech_db.* TO 'nucleotech_user'@'localhost';
    FLUSH PRIVILEGES;
    EXIT;
    ```
    *Nota: A senha 'password' é para fins de desenvolvimento.*

6.  **Aplique as Migrações do Django**:
    ```bash
    python manage.py migrate
    ```

7.  **Crie um superusuário (opcional, para acessar o painel administrativo do Django)**:
    ```bash
    python manage.py createsuperuser
    ```
    *Siga as instruções para criar o superusuário.*

8.  **Inicie o servidor de desenvolvimento do Django**:
    ```bash
    python manage.py runserver
    ```

### Acessando o Frontend

Após iniciar o servidor Django, abra seu navegador e acesse `http://127.0.0.1:8000/`. Você será redirecionado para a página de login do frontend.

### Testando as Funcionalidades

- **Cadastro e Login**: Utilize as páginas de `register.html` e `login.html` para criar uma conta e fazer login.
- **Processamento de Imagens e Áudio**: Na página `tools.html`, faça upload de arquivos e utilize as ferramentas de processamento. Os resultados serão exibidos e estarão disponíveis para download.
- **Histórico**: A página `history.html` (atualmente com um placeholder) deverá ser implementada para exibir o histórico de processamento do usuário.

## Estrutura de Pastas Final

```
project/
├── backend/
│   ├── nucleotech_project/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── users/
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── services/
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   ├── processing/
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   └── subscriptions/
│       ├── migrations/
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── tests.py
│       └── views.py
├── frontend/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── auth.js
│   │   └── processing.js
│   ├── pages/
│   │   ├── dashboard.html
│   │   ├── history.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── tools.html
│   └── index.html
├── tools/
│   ├── audio_tools.py
│   └── image_tools.py
├── manage.py
├── README.md
└── venv/
```
