# Modern FastAPI Boilerplate (Spring Boot Style)

Uma aplicação backend em Python construída com as tecnologias e arquiteturas mais modernas do mercado. O objetivo deste projeto é prover uma fundação extremamente robusta, escalável e de altíssima performance, utilizando processamento 100% assíncrono, mas com uma **Developer Experience (DX) inspirada no Spring Boot (Java)**.

A arquitetura foi projetada para focar na **Limpeza de Código e Inversão de Controle**. Em vez de poluir o código passando variáveis de banco de dados (`db_session`) entre todas as camadas, a aplicação utiliza ContextVars para gerenciar o estado da requisição de forma implícita e automática, permitindo que a regra de negócio fique totalmente isolada da infraestrutura.

## 🛠 Tecnologias Utilizadas

*   **[FastAPI](https://fastapi.tiangolo.com/):** Framework web de altíssima performance.
*   **[Uvicorn](https://www.uvicorn.org/):** Servidor ASGI super rápido, agindo como o coração de execução da aplicação.
*   **[SQLAlchemy 2.0 (Async)](https://www.sqlalchemy.org/):** ORM para bancos de dados operando de forma 100% assíncrona (`asyncpg`).
*   **[fastapi-utils](https://fastapi-utils.davidmontague.xyz/):** Fornece os utilitários de **Class Based Views (CBV)**, emulando o comportamento de classes e injeção do Spring Boot.
*   **[Alembic Internals](https://alembic.sqlalchemy.org/):** Ferramenta de migrações instanciada dinamicamente *em memória* para atualização de DDL em tempo real.
*   **[Beanie](https://beanie-odm.dev/) & [Motor](https://motor.readthedocs.io/):** ODM assíncrono para o MongoDB.
*   **[Pydantic V2](https://docs.pydantic.dev/):** Validação de dados rigorosa através de Data Transfer Objects (DTOs).

## 📐 Arquitetura

O projeto segue uma padronização madura baseada em **Camadas (Layered Architecture)** com forte inspiração no ecosistema Spring:

1.  **Controllers (`app/controllers`):** Ponto de entrada HTTP utilizando **Class Based Views (`@cbv`)**. Classes injetam `Services` nativamente via `Depends()` e centralizam rotas com `InferringRouter`.
2.  **Services (`app/services`):** Onde mora toda a Regra de Negócio. Totalmente isoladas da camada HTTP.
3.  **Repositories (`app/repositories`):** Camada de dados responsável pelas queries no SQLAlchemy recuperando a sessão ativa magicamente do `ContextVar`.
4.  **DTOs (`app/dtos`):** Objetos de Transferência de Dados (`Pydantic Models`).
5.  **Models (`app/models`):** Modelos `DeclarativeBase` mesclados com Dataclasses baseados em chaves nomeadas.

### ✨ Destaques de Arquitetura
*   **Emulação `hibernate.hbm2ddl.auto`:** Atualizações de banco de dados (`ADD COLUMN`, `CREATE TABLE`) feitas automaticamente em tempo de execução durante o `lifespan` do FastAPI. Nenhum arquivo físico `.py` de migração é gerado. Alterou o modelo, o banco atualiza na inicialização.
*   **Gerenciamento de Transação Automático via Middleware:** Um *Middleware* intercepta a requisição, abre a sessão no banco, armazena num `ContextVar` e, ao fim, executa commit ou rollback automaticamente.
*   **Roteamento Centralizado (Explicit Routing):** Padrão canônico do FastAPI usando `__init__.py` dentro de `app/controllers` para agregar os `APIRoutes` limpos, garantindo facilidade de rastreio na IDE (Ctrl+Click).

## ⚙️ Como Executar o Projeto

### Pré-requisitos
*   [Python 3.10+](https://www.python.org/)
*   [uv](https://github.com/astral-sh/uv) (Recomendado como gerenciador de pacotes)
*   Bancos de dados rodando (PostgreSQL e MongoDB)

### 1. Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto e configure as conexões baseadas na classe `Settings`:

```env
APP_ENV=development

# Postgres
DB_URL=postgresql+asyncpg://seu_usuario:sua_senha@localhost:5432/seu_banco
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_ECHO=True
DB_POOL_PRE_PING=True

# DDL Auto (Emulador Mapeamento JPA)
# Opções: create, update, none
ALEMBIC_DDL_AUTO=update

# MongoDB (Logs)
ENABLE_MONGO_LOGS=True
MONGODB_URL=mongodb://localhost:27017
MONGO_DB_NAME=logs_db
```

### 2. Instalação das Dependências

Usando `uv` (muito mais rápido):
```bash
uv sync 
```

### 3. Rodando a Aplicação
Execute o servidor Uvicorn com hot-reload ativo para desenvolvimento:

```bash
uv run uvicorn app.main:app --reload
```

Acesse a documentação interativa oficial (Swagger UI) gerada automaticamente na rota:
**http://localhost:8000/docs**

## 📁 Estrutura de Pastas

```
├── app/
│   ├── configs/          # Configurações DB, DDLManager, Middlewares e Lifespan
│   ├── controllers/      # Controladores REST baseados em Classes (CBV) agregados via __init__.py
│   ├── dtos/             # Data Transfer Objects (Pydantic)
│   ├── exceptions/       # Custom Exception Handlers
│   ├── models/           # Models SQLAlchemy 2.0 (Dataclasses) e Beanie
│   ├── repositories/     # Padrão Repository interagindo com ContextVars
│   ├── services/         # Lógica de Negócios Centralizada
│   ├── utils/            # Ferramentas auxiliares (ex: Patch de DTOs)
│   └── main.py           # Entrypoint super limpo (inclui routes e middlewares)
├── pyproject.toml        # Configuração de pacotes
├── requirements.txt      # Dependências exportadas
└── .env                  # Variáveis de ambiente secretas
```