# Modern FastAPI Boilerplate

Uma aplicação backend em Python construída com as tecnologias e arquiteturas mais modernas do mercado. O objetivo deste projeto é prover uma fundação extremamente robusta, escalável e de altíssima performance, utilizando processamento 100% assíncrono.

A arquitetura foi projetada para focar na **Limpeza de Código e Inversão de Controle**. Em vez de poluir o código passando variáveis de banco de dados (`db_session`) entre todas as camadas, a aplicação utiliza ContextVars para gerenciar o estado da requisição de forma implícita e automática, permitindo que a regra de negócio fique totalmente isolada da infraestrutura.

## 🛠 Tecnologias Utilizadas

*   **[FastAPI](https://fastapi.tiangolo.com/):** Framework web de altíssima performance.
*   **[Uvicorn](https://www.uvicorn.org/):** Servidor ASGI super rápido, agindo como o coração de execução da aplicação.
*   **[SQLAlchemy 2.0 (Async)](https://www.sqlalchemy.org/):** ORM para bancos de dados relacionais (PostgreSQL) usando a nova sintaxe declarativa operando de forma 100% assíncrona (`asyncpg`).
*   **[Beanie](https://beanie-odm.dev/) & [Motor](https://motor.readthedocs.io/):** ODM assíncrono para o MongoDB, utilizado para sistemas de logs escaláveis.
*   **[Pydantic V2](https://docs.pydantic.dev/):** Validação de dados rigorosa através de Data Transfer Objects (DTOs).
*   **[uv](https://github.com/astral-sh/uv):** Gerenciador de pacotes ultrarrápido escrito em Rust.

## 📐 Arquitetura

O projeto segue uma padronização madura baseada em **Camadas (Layered Architecture)**:

1.  **Controllers (`app/controllers`):** Ponto de entrada HTTP da aplicação (Rotas do FastAPI). Apenas recebem a requisição, delegam para o Service e retornam a resposta.
2.  **Services (`app/services`):** Onde mora toda a Regra de Negócio. Instanciadas como *Singletons*, não sabem nada sobre HTTP ou Bancos de Dados diretamente.
3.  **Repositories (`app/repositories`):** Especializados em comunicar com o banco de dados. Recuperam magica e automaticamente a sessão ativa do Contexto da Requisição.
4.  **DTOs (`app/dtos`):** Objetos de Transferência de Dados, isolando os Modelos de Banco de Dados da visualização JSON externa.
5.  **Models (`app/models`):** Modelos ORM (SQLAlchemy) que refletem as tabelas físicas.

### ✨ Destaques de Arquitetura
*   **Gerenciamento de Transação Automático:** Um *Middleware* intercepta a requisição, abre a sessão no banco, armazena num `ContextVar` e, ao fim, comita ou dá erro (rollback), fechando a sessão de forma segura sem `try/excepts` espalhados.
*   **Auto-Scan de Entidades:** O app mapeia modelos automaticamente no boot e cria tabelas estruturais de forma autônoma sem necessitar de dezenas de imports manuais em scripts de inicialização.
*   **Modelagem de Logs Distribuída:** Separação de responsabilidade onde dados relacionais vão pro SQL e logs brutos vão de maneira não-bloqueante para o MongoDB.

## ⚙️ Como Executar o Projeto

### Pré-requisitos
*   [Python 3.10+](https://www.python.org/)
*   [uv](https://github.com/astral-sh/uv) (Opcional, mas recomendado como gerenciador de pacotes)
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
DDL_AUTO_CREATE=True 

# MongoDB (Logs)
ENABLE_MONGO_LOGS=True
MONGODB_URL=mongodb://localhost:27017
MONGO_DB_NAME=logs_db
```

### 2. Instalação das Dependências

Usando `uv` (rápido):
```bash
uv sync  # ou `uv pip install -r requirements.txt`
```

Ou usando o pip tradicional:
```bash
pip install -r requirements.txt
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
│   ├── controllers/      # Controladores REST (APIRouters)
│   ├── core/             # Configurações, injeções, setups de Banco de Dados
│   ├── dtos/             # Data Transfer Objects (Request/Response schemas)
│   ├── models/           # Models ORM (SQLAlchemy e Beanie)
│   ├── repositories/     # Camada de abstração do Banco de Dados
│   ├── services/         # Lógica de Negócios Central
│   ├── main.py           # Ponto de inicialização do app (Lifespan e Middlewares)
├── pyproject.toml        # Configuração de pacotes
├── requirements.txt      # Dependências exportadas
└── .env                  # Variáveis de ambiente secretas
```