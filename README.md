# LuEstilo - API Backend

Esta é a API backend desenvolvida para a empresa Lu Estilo, responsável por gerenciar clientes, produtos, pedidos e integrações com WhatsApp.

---

## Tecnologias

* **[FastAPI](https://fastapi.tiangolo.com/)**
* **PostgreSQL**
* **SQLAlchemy**
* **Pydantic v2**
* **JWT (python-jose)**
* **Docker & Docker Compose**
* **Alembic**
* **Pytest**

---

## Instalação local (sem Docker)

### 1. Clone o projeto

```bash
git clone https://github.com/seu-usuario/lu-estilo-api.git
cd lu-estilo-api
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/macOS
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o `.env`

Crie um arquivo `.env` com:

```env
DATABASE_URL=postgresql://postgres:sua_senha@localhost:5432/luestilo
SECRET_KEY=chave_jwt_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Rode as migrações

```bash
alembic upgrade head
```

### 6. Inicie a aplicação

```bash
uvicorn app.main:app --reload
```

Acesse: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Executando com Docker

### 1. Ajuste o `.env` para ambiente Docker:

```env
DATABASE_URL=postgresql://postgres:sua_senha@db:5432/luestilo
```

### 2. Suba os serviços

```bash
docker-compose up --build
```

### 3. Acesse a aplicação

* Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Aplique as migrações (dentro do contêiner)

```bash
docker-compose exec web alembic upgrade head
```

---

## Rodando os testes

```bash
pytest -v
```

Todos os testes estão em `tests/`, incluindo:

* Autenticação
* Clientes
* Produtos
* Pedidos

---

## Integração com WhatsApp (opcional)

 Integração real não foi ativada por falta de sinal móvel para validar o número via Facebook Developer.

## Autenticação
Via OAuth2 Password Flow:

- Rota de login: /auth/login (com grant_type=password)

- Swagger Authorize com Bearer Token

Usuários:

- admin → pode criar/editar/excluir

- comum → apenas visualizar

-

```

---

## Endpoints principais

| Método | Rota           | Descrição                  |
| ------ | -------------- | -------------------------- |
| POST   | /auth/register | Registrar usuário          |
| POST   | /auth/login    | Login (retorna JWT)        |
| GET    | /clients       | Listar clientes            |
| POST   | /clients       | Criar cliente              |
| GET    | /products      | Listar produtos            |
| POST   | /products      | Criar produto              |
| GET    | /orders        | Listar pedidos             |
| POST   | /orders        | Criar pedido (com estoque) |

---

## Autenticação

Quase todos os endpoints exigem token JWT:

1. Registre e faça login
2. No Swagger (`/docs`), clique em **Authorize**
3. Informe os dados assim (segue as mesmas regras de usuarios normais e admin)

```
username
senha
```

---

## Autor

Gabriel Leonardo Cunha Santos
Projeto de avaliação técnica — Backend
