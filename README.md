# Modern FastAPI Boilerplate (Spring Boot Style)

Uma aplicação backend em Python construída com as tecnologias e arquiteturas mais modernas do mercado. O objetivo deste projeto é prover uma fundação extremamente robusta, escalável e de altíssima performance, utilizando processamento 100% assíncrono, mas com uma **Developer Experience (DX) inspirada no Spring Boot (Java)**.

A arquitetura foi projetada para focar na **Limpeza de Código e Inversão de Controle**. Em vez de poluir o código passando variáveis de banco de dados (`db_session`) entre todas as camadas, a aplicação utiliza ContextVars para gerenciar o estado da requisição de forma implícita e automática, permitindo que a regra de negócio fique totalmente isolada da infraestrutura.

## 🛠 Tecnologias Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/):** Framework web de altíssima performance.
- **[Uvicorn](https://www.uvicorn.org/):** Servidor ASGI super rápido, agindo como o coração de execução da aplicação.
- **[SQLAlchemy 2.0 (Async)](https://www.sqlalchemy.org/):** ORM para bancos de dados operando de forma 100% assíncrona (`asyncpg`).
- **[fastapi-utils](https://fastapi-utils.davidmontague.xyz/):** Fornece os utilitários de **Class Based Views (CBV)**, emulando o comportamento de classes e injeção do Spring Boot.
- **[Alembic Internals](https://alembic.sqlalchemy.org/):** Ferramenta de migrações instanciada dinamicamente *em memória* para atualização de DDL em tempo real.
- **[Beanie](https://beanie-odm.dev/) & [Motor](https://motor.readthedocs.io/):** ODM assíncrono para o MongoDB.
- **[Pydantic V2](https://docs.pydantic.dev/):** Validação de dados rigorosa através de Data Transfer Objects (DTOs).

## 📐 Arquitetura

O projeto segue uma padronização madura baseada em **Camadas (Layered Architecture)** com forte inspiração no ecosistema Spring:

1. **Controllers (`app/controllers`):** Ponto de entrada HTTP utilizando **Class Based Views (`@cbv`)**. Classes injetam `Services` nativamente via `Depends()` e centralizam rotas com `InferringRouter`.
1. **Services (`app/services`):** Onde mora toda a Regra de Negócio. Totalmente isoladas da camada HTTP.
1. **Repositories (`app/repositories`):** Camada de dados responsável pelas queries no SQLAlchemy recuperando a sessão ativa magicamente do `ContextVar`.
1. **DTOs (`app/dtos`):** Objetos de Transferência de Dados (`Pydantic Models`).
1. **Models (`app/models`):** Modelos `DeclarativeBase` mesclados com Dataclasses baseados em chaves nomeadas.

### ✨ Destaques de Arquitetura

- **Emulação `hibernate.hbm2ddl.auto`:** Atualizações de banco de dados (`ADD COLUMN`, `CREATE TABLE`) feitas automaticamente em tempo de execução durante o `lifespan` do FastAPI. Nenhum arquivo físico `.py` de migração é gerado. Alterou o modelo, o banco atualiza na inicialização.
- **Gerenciamento de Transação Automático via Middleware:** Um *Middleware* intercepta a requisição, abre a sessão no banco, armazena num `ContextVar` e, ao fim, executa commit ou rollback automaticamente.
- **Roteamento Centralizado (Explicit Routing):** Padrão canônico do FastAPI usando `__init__.py` dentro de `app/controllers` para agregar os `APIRoutes` limpos, garantindo facilidade de rastreio na IDE (Ctrl+Click).

## ⚙️ Como Executar o Projeto

### Pré-requisitos

- [Python 3.10+](https://www.python.org/)
- [uv](https://github.com/astral-sh/uv) (Recomendado como gerenciador de pacotes)
- Bancos de dados rodando (PostgreSQL e MongoDB)

### 1. Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto e configure as conexões baseadas na classe `Settings`:

```env
# App
APP_ENV=local
APP_VERSION=1.0.0
UVICORN_WORKERS=4
UVICORN_HOST=0.0.0.0
UVICORN_PORT=5000
LOG_LEVEL=INFO

# Database
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=seu_host
DB_PORT=5432
DB_NAME=seu_banco

DB_POOL_SIZE=20
DB_MAX_OVERFLOW=40
DB_ECHO=False
DB_POOL_PRE_PING=True

ALEMBIC_DDL_AUTO=update

# MongoDB
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=replace_with_strong_mongo_password
MONGO_DB_NAME=logs_db
MONGO_TIMEOUT_MS=5000
ENABLE_MONGO_LOGS=False
MONGODB_URL=mongodb://admin:replace_with_strong_mongo_password@mongodb:27017/?authSource=admin
```

### 2. Instalação das Dependências

Usando `uv` (muito mais rápido):

```bash
uv sync
```

Como o projeto utiliza o `pre-commit` para assegurar a qualidade do código (formatação, linting, checagens estáticas), ative os hooks locais antes de começar a trabalhar:

```bash
uv run pre-commit install
```

### 3. Rodando a Aplicação

O projeto possui um entrypoint limpo e age como um módulo Python fechado. Você pode iniciar o servidor de duas formas:

Executando o módulo `app` (repassando para o `__main__.py`):

```bash
uv run python -m app
```

Ou através do comando nativo gerado pelo pacote UV:

```bash
uv run app
```

Acesse a documentação interativa oficial (Swagger UI) gerada automaticamente na rota:
**http://localhost:8000/docs**

### 4. Rodando no Docker (Produção)

A aplicação conta com um ambiente robusto utilizando contêineres de produção (*non-root user*, `tini`, limites e configs).

```bash
# Build e execução convencional da API + DB
./docker/run.sh

# Build e execução utizando pacotes otimizados em modo Wheel (.whl), estilo empacotamento "Java .jar"
./docker/run.sh --wheel
```

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
│   ├── __init__.py       # Fastapi limpo (Declaração de contexto, Middleware, Roteador)
│   └── __main__.py       # Entrypoint executável que chama o uvicorn nativamente
├── docker/               # Configurações para Docker (Compose, Multi-stage e .whl builds)
├── pyproject.toml        # Configuração de pacotes e entrada de compilação
├── requirements.txt      # Dependências exportadas
└── .env                  # Variáveis de ambiente secretas
```
