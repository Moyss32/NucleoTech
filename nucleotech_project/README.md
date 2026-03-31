# NucleoTech - Commit 1: Estrutura Base

Este commit estabelece a estrutura base do projeto SaaS "NucleoTech", incluindo a configuração inicial do Django, banco de dados MySQL, e os modelos de dados para Usuários, Assinaturas, Serviços e Processamento.

## Conteúdo do Commit

- **Configuração do Projeto Django**: Inicialização do projeto Django `nucleotech_project`.
- **Aplicativos Django**: Criação dos aplicativos `users`, `services`, `processing` e `subscriptions`.
- **Configuração do Banco de Dados MySQL**: Configuração do `settings.py` para utilizar MySQL como banco de dados, com o banco `nucleotech_db` e o usuário `nucleotech_user`.
- **Modelos de Dados**: Definição dos modelos de dados nos respectivos aplicativos:
    - `users/models.py`: Modelo `User` (estendendo `AbstractUser`).
    - `subscriptions/models.py`: Modelo `Subscription`.
    - `services/models.py`: Modelos `Service`, `Aplicativo` e `Service_App`.
    - `processing/models.py`: Modelos `Uso_Servico`, `Execucao_Local`, `Arquivo_Processado` e `Resultado_Processamento`.
- **Migrações**: Geração e aplicação das migrações iniciais para criar as tabelas no banco de dados.

## Como Configurar e Rodar o Projeto (Commit 1)

### Pré-requisitos

- Python 3.11
- MySQL Server

### Passos de Configuração

1.  **Clone o repositório** (ou descompacte o arquivo `commit_1.zip`).

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
    pip install Django mysqlclient
    ```
    *Se houver erros na instalação do `mysqlclient`, certifique-se de que os pacotes de desenvolvimento do MySQL e Python estejam instalados:*
    ```bash
    sudo apt-get update
    sudo apt-get install -y libmysqlclient-dev pkg-config build-essential python3.11-dev
    pip install mysqlclient
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
    *Nota: A senha 'password' é para fins de desenvolvimento. Em produção, use uma senha forte e segura.*

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

Agora o projeto base está configurado e o servidor Django deve estar rodando em `http://127.0.0.1:8000/`.
