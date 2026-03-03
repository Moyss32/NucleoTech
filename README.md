# NucleoTech - Soluções Tecnológicas

NucleoTech é uma plataforma profissional de venda de softwares, desenvolvida com um backend robusto em Python (Flask) e um frontend moderno e minimalista utilizando apenas HTML, CSS e JavaScript puros.

## 🚀 Funcionalidades

- **Página Inicial**: Hero section impactante, seção sobre, destaques de produtos e depoimentos.
- **Catálogo de Produtos**: Listagem dinâmica com filtros por categoria.
- **Detalhes do Produto**: Informações detalhadas, benefícios e especificações.
- **Sistema de Autenticação**: Cadastro de usuários e login seguro com hash de senha.
- **Área do Usuário**: Perfil com histórico de pedidos.
- **Painel Administrativo**: Gestão completa de produtos (CRUD), visualização de usuários e pedidos.
- **API REST**: Comunicação eficiente entre frontend e backend.
- **Design Responsivo**: Otimizado para desktop e dispositivos móveis.

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.11, Flask, SQLAlchemy (ORM), Flask-Login, Flask-Bcrypt.
- **Frontend**: HTML5, CSS3 (Variáveis, Flexbox, Grid), JavaScript (Fetch API).
- **Banco de Dados**: SQLite (Fácil configuração local).

## 📁 Estrutura do Projeto

```text
nucleotech/
├── app/
│   ├── models/          # Modelos do Banco de Dados (MVC)
│   ├── routes/          # Rotas da API e Páginas (MVC)
│   ├── static/          # Arquivos estáticos (CSS, JS, Imagens)
│   ├── templates/       # Templates HTML
│   └── __init__.py      # Inicialização do Flask
├── instance/            # Banco de Dados SQLite
├── config.py            # Configurações do sistema
├── run.py               # Script para rodar o servidor
├── seed.py              # Script para popular o banco de dados
└── requirements.txt     # Dependências do projeto
```

## 🏃 Como Rodar o Projeto

1. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Prepare o Banco de Dados**:
   Execute o script de semente para criar as tabelas e adicionar produtos iniciais:
   ```bash
   python seed.py
   ```
   *Isso também criará um usuário administrador padrão:*
   - **Email**: `admin@nucleotech.com`
   - **Senha**: `admin123`

3. **Inicie o Servidor**:
   ```bash
   python run.py
   ```

4. **Acesse o Site**:
   Abra o navegador em `http://127.0.0.1:5000`

## 🔒 Segurança

- Senhas são armazenadas utilizando **Bcrypt** (hashing seguro).
- Proteção de rotas administrativas e de usuário.
- Separação clara entre lógica de negócio (backend) e apresentação (frontend).
