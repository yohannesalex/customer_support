# Support Assistant Backend

## Overview
This repository contains a FastAPI-based backend service for a customer support assistant. It features:

- **User Authentication** (signup/login via JWT)
- **Support Ticket Management** (create, retrieve tickets and messages)
- **Real-time AI Response Streaming** (using SSE and Groq API)
- **Modular, OOP-Driven Architecture**
- **Containerization** with Docker/Docker Compose

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yohannesalex/customer_support
   cd support_assistant_backend
   ```

2. **Environment Variables**:
   - Copy the template:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and set:
     ```
     POSTGRES_USER=<your_db_user>
     POSTGRES_PASSWORD=<your_db_password>
     POSTGRES_DB=<your_db_name>
     DATABASE_URL=postgresql+asyncpg://$POSTGRES_USER:$POSTGRES_PASSWORD@db:5432/$POSTGRES_DB
     SECRET_KEY=<your_jwt_secret>
     GROQ_API_KEY=<your_groq_api_key>
     ```


3. **Run the Application**:
   - With Docker Compose:
     ```bash
     docker-compose up --build
     ```
        This will build the Docker image, apply any pending Alembic migrations via the entrypoint.sh script, and start the FastAPI application.

        Or directly (for local development):

```bash

alembic upgrade head
uvicorn support_assistant_backend.main:app --reload   - Or directly (for local dev):
```
     ```bash
     uvicorn backend.main:app --reload
     ```

4. **Testing**:
   ```bash
   pytest
   ```

---

## Architecture & OOP Principles

- **Layered Modules**: Separation of concerns in `models`, `schemas`, `services`, `routes`, `utils`, and `core` config.
- **Dependency Injection**: FastAPI `Depends` for DB sessions and user auth.
- **Service Classes**: Encapsulate business logic in `AuthService`, `TicketService`, `MessageService`, `AIService`.
- **Pydantic Schemas**: Strong validation and serialization logic.
- **Automatic Table Naming**: `Base` class generates `__tablename__` from model names.

---

## Design Patterns

- **Service/Repository Pattern**: Services handle data operations, keeping route handlers lean.
- **Factory for JWT**: `create_access_token` centralizes token generation.
- **Strategy for AI**: `AIService` abstracts AI-provider specifics, allowing pluggable implementations.

---

## Challenges & Solutions

- **Async Migrations**: Configured Alembic `env.py` to use SQLAlchemy Async engine for autogeneration.
- **SSE Streaming**: Tuned FastAPI’s `StreamingResponse` for smooth AI chunk delivery.
- **Secret Management**: Consolidated all secrets into `.env`, loaded via Docker Compose `env_file`.

---

## Future Improvements
- **handling different cases in api request and response**: Due to time limitation i handled basic api response cases
- **Advanced RBAC**: Fine-grained permissions beyond admin/user roles.
- **Enhanced Prompt Context**: Include full message history in AI prompts for richer responses.
- **Caching & Rate Limiting**: Integrate Redis for performance and protection against abuse.
- **CI/CD Workflow**: Automated tests, linting, and deployments via GitHub Actions.

---

## Documentation & Comments

- Code is annotated with inline comments where complex logic exists.
- FastAPI’s OpenAPI docs are available at `/docs` when the server is running.
- See `README.md` and in-code docstrings for further details.

