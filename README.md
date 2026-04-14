# NucleoTech - Commit 2: Autenticação e API de Usuários

Este commit implementa o sistema de autenticação JWT e a API para gerenciamento de usuários, permitindo o cadastro, login e visualização de perfil.

## Conteúdo do Commit

- **Integração do Django Rest Framework (DRF)**: Configuração do DRF para construção de APIs.
- **Autenticação JWT**: Implementação de `djangorestframework-simplejwt` para autenticação baseada em tokens.
- **Serializadores de Usuário**: Criação de `UserSerializer` para lidar com a criação e representação de dados de usuários.
- **Views de Autenticação**:
    - `RegisterView`: Endpoint para criação de novas contas de usuário.
    - `UserProfileView`: Endpoint para visualizar e atualizar o perfil do usuário autenticado.
    - `TokenObtainPairView` e `TokenRefreshView`: Endpoints padrão do SimpleJWT para login e renovação de tokens.
- **Roteamento de API**: Configuração das URLs para os novos endpoints de usuário em `api/users/`.

## Como Testar a Autenticação (Commit 2)

### Pré-requisitos

- Siga os passos de configuração do **Commit 1**.
- Instale as novas dependências:
    ```bash
    pip install djangorestframework djangorestframework-simplejwt
    ```

### Endpoints Disponíveis

- **Cadastro**: `POST /api/users/register/`
    - Corpo: `{"username": "seu_usuario", "password": "sua_senha", "email": "seu@email.com"}`
- **Login (Obter Token)**: `POST /api/users/login/`
    - Corpo: `{"username": "seu_usuario", "password": "sua_senha"}`
    - Retorna: `access` e `refresh` tokens.
- **Renovar Token**: `POST /api/users/token/refresh/`
    - Corpo: `{"refresh": "seu_refresh_token"}`
- **Perfil do Usuário**: `GET /api/users/profile/`
    - Requer Header: `Authorization: Bearer <seu_access_token>`

### Exemplo de Uso com `curl`

1.  **Cadastrar**:
    ```bash
    curl -X POST http://127.0.0.1:8000/api/users/register/ -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpassword123"}'
    ```

2.  **Login**:
    ```bash
    curl -X POST http://127.0.0.1:8000/api/users/login/ -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpassword123"}'
    ```

3.  **Acessar Perfil** (substitua `<access_token>` pelo token recebido no login):
    ```bash
    curl -X GET http://127.0.0.1:8000/api/users/profile/ -H "Authorization: Bearer <access_token>"
    ```
