# Tasks API

REST API for task management (TODOs) developed with FastAPI and PostgreSQL.

## 🚀 Installation and Execution

### Prerequisites

- Docker and Docker Compose
- Python 3.12
- PostgreSQL (only if not using Docker)

### Using Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd tasks
   ```

2. Start the services with Docker Compose:
   ```bash
   docker-compose up -d
   ```

   This will start the following services:
   - API at http://localhost:8000
   - PostgreSQL at localhost:5432
   - Adminer (PostgreSQL web interface) at http://localhost:8080

3. Verify the API is running:
   ```bash
   curl http://localhost:8000/health
   ```

### Without Docker

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies using `uv` (recommended) or `pip`:

   Using `uv` (faster and more efficient):
   ```bash
   # Install uv if not already installed
   pip install uv
   # Or use the official installer:
   # curl -LsSf https://astral.sh/uv/install.sh | sh

   # Sync dependencies from uv.lock
   uv sync

3. Configure environment variables in a `.env` file.

4. Run Alembic migrations:
   ```bash
   alembic upgrade head
   ```

5. Start the server:
   ```bash
   # Using uv to run the server
   uv run uvicorn main:app --reload

   # Or activate the virtual environment and run normally
   uvicorn main:app --reload
   ```

## 📚 API Documentation

Interactive API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔐 Authentication

The API uses JWT authentication. To authenticate:

1. Register a new user:
   ```bash
   curl -X 'POST' \
     'http://localhost:8000/users' \
     -H 'Content-Type: application/json' \
     -d '{
       "email": "user@example.com",
       "password": "secure-password"
     }'
   ```

2. Login to get your JWT token:
   ```bash
   curl -X 'POST' \
     'http://localhost:8000/auth/login' \
     -H 'Content-Type: application/json' \
     -d '{
       "email": "user@example.com",
       "password": "secure-password"
     }'
   ```

3. Use the token in your request headers:
   ```
   Authorization: Bearer <your-jwt-token>
   ```

## 📝 Usage Examples

### Create a Task
```bash
curl -X 'POST' \
  'http://localhost:8000/tasks' \
  -H 'Authorization: Bearer <token>' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "My first task",
    "description": "This is an example description",
  }'
```

### List Tasks (with pagination)
```bash
curl -X 'GET' \
  'http://localhost:8000/tasks?page=1&page_size=10' \
  -H 'Authorization: Bearer <token>'
```

### Get Task by ID
```bash
curl -X 'GET' \
  'http://localhost:8000/tasks/<task-id>' \
  -H 'Authorization: Bearer <token>'
```

### Update a Task
```bash
curl -X 'PUT' \
  'http://localhost:8000/tasks/<task-id>' \
  -H 'Authorization: Bearer <token>' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Updated title",
    "status": "COMPLETED"
  }'
```

### Delete a Task
```bash
curl -X 'DELETE' \
  'http://localhost:8000/tasks/<task-id>' \
  -H 'Authorization: Bearer <token>'
```

## 🛠️ Project Structure

This project follows a **modular architecture inspired by NestJS**, providing excellent organization, scalability, and maintainability for Python FastAPI applications.

```
.
# Root files
alembic.ini              # Alembic configuration
docker-compose.yml       # Docker Compose configuration
Dockerfile              # Container configuration
main.py                 # Application entry point
pyproject.toml          # Project metadata and dependencies
README.md               # Project documentation
run.py                  # Application runner
uv.lock                 # Dependency lock file

# Source code
src/
├── common/             # Common utilities and dependencies
│   ├── dependencies.py # Common FastAPI dependencies
│   └── pagination.py   # Pagination utilities
│
├── core/               # Core application configuration
│   ├── config.py       # Application configuration
│   └── logging.py      # Logging configuration
│
├── db/                 # Database configuration and models
│   ├── alembic/        # Database migrations
│   ├── base.py         # SQLAlchemy base models
│   ├── models.py       # Database models
│   └── session.py      # Database session management
│
├── modules/            # Application modules (NestJS-inspired)
│   ├── auth/           # Authentication module
│   │   ├── dependencies.py  # Auth dependencies
│   │   ├── repository.py    # Auth data access
│   │   ├── router.py        # Auth API routes (Controller)
│   │   └── service.py       # Auth business logic (Service)
│   │
│   ├── tasks/          # Tasks module
│   │   ├── dto.py      # Data transfer objects
│   │   ├── model.py    # Task models (Entity)
│   │   ├── repository.py    # Data access layer
│   │   ├── router.py        # API routes (Controller)
│   │   ├── schema.py        # Pydantic schemas (DTO)
│   │   └── service.py       # Business logic (Service)
│   │
│   └── users/          # Users module
│       ├── dto.py
│       ├── model.py
│       ├── repository.py
│       ├── router.py
│       └── service.py
│
└── tests/              # Test suite
    └── unit/           # Unit tests
        ├── auth/       # Auth tests
        ├── tasks/      # Tasks tests
        └── users/      # Users tests

# Logs
logs/
├── audit.log          # Audit trail logs
└── errors.log         # Error logs
```

### 🏗️ NestJS-Inspired Architecture Benefits

This modular structure, inspired by **NestJS** (Node.js framework), brings enterprise-grade organization to Python FastAPI:

#### **📦 Module-Based Organization**
- **Clear Separation**: Each feature (auth, tasks, users) is self-contained
- **Scalability**: Easy to add new modules without affecting existing code
- **Team Development**: Multiple developers can work on different modules simultaneously

#### **🔄 Layered Architecture Pattern**
- **Router (Controller)**: Handles HTTP requests and responses
- **Service**: Contains business logic and orchestrates operations
- **Repository**: Manages data access and database operations
- **Model (Entity)**: Defines database schema and relationships
- **Schema/DTO**: Handles data validation and serialization

#### **🎯 Key Advantages**
- **Maintainability**: Code is organized logically and easy to navigate
- **Testability**: Each layer can be tested independently with clear boundaries
- **Reusability**: Services and repositories can be shared across different modules
- **Dependency Injection**: Clean separation of concerns with FastAPI's DI system
- **Enterprise Ready**: Follows proven patterns from enterprise Node.js applications

#### **🔧 Consistency**
- **Predictable Structure**: Every module follows the same pattern
- **Developer Onboarding**: New team members can quickly understand the codebase
- **Code Standards**: Consistent naming and organization conventions

## 🧪 Testing

### Logging in Tests

By default, logging is disabled during test execution to keep the test output clean. This is controlled by the `DISABLE_LOGS` environment variable which defaults to `true`.

To enable logging during tests:

```bash
# Enable logging for a single test run
DISABLE_LOGS=false pytest

# Or set it permanently in your shell
export DISABLE_LOGS=false
```

### Test Database

The test database is automatically created and dropped during test execution.

### Test Fixtures

The test suite includes several useful fixtures:

- `db`: Provides a fresh database session for each test
- `client`: Provides a test HTTP client with database session
- `db_user`: Creates a test user in the database
- `create_test_token`: Helper function to create JWT tokens for testing

### Running Tests

To run the unit tests:

```bash
# Using uv
uv run pytest src/tests/

# Or with traditional method
pytest src/tests/
```

For specific test categories:
```bash
# Run only unit tests
uv run pytest src/tests/unit/

# Run tests in verbose mode
uv run pytest src/tests/ -v
```

## 📊 Database Migrations

The project uses Alembic for database migrations. To create a new migration:

```bash
# Using uv
uv run alembic revision --autogenerate -m "description of changes"
uv run alembic upgrade head

# Or traditional method
alembic revision --autogenerate -m "description of changes"
alembic upgrade head
```

## 🔧 Development Commands

Common development tasks using uv:

```bash
# Install development dependencies
uv sync --group dev

# Add a new dependency
uv add fastapi

# Add a development dependency
uv add --group dev pytest

# Update dependencies
uv sync --upgrade

# Run linting
uv run ruff check src/
uv run ruff format src/

# Run type checking
uv run mypy src/
```

## ⚡ Why use uv?

This project uses [uv](https://github.com/astral-sh/uv) for dependency management because it offers significant advantages:

- **Blazing Fast**: uv is written in Rust and provides much faster dependency resolution and installation than pip
- **Reliable**: Uses modern dependency resolution algorithms to avoid dependency conflicts
- **Consistent**: Ensures reproducible builds across different environments with `uv.lock`
- **Efficient**: Implements advanced caching and parallel downloads
- **Modern**: Built with modern Python packaging standards in mind
- **Virtual Environment Management**: Automatically manages virtual environments
- **Cross-platform**: Works consistently on Windows, macOS, and Linux

## 🔒 Environment Variables

Copy the `.env.example` file to `.env` and configure the following variables:

```env
# Database configuration
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/tasks_db

# Authentication configuration
SECRET_KEY=your-secret-key-here-make-it-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application configuration
ENVIRONMENT=development
LOG_LEVEL=INFO
```

## 🚀 Quick Start

For the fastest setup:

```bash
# 1. Install uv if you haven't already
pip install uv

# 2. Clone and navigate to project
git clone <repo-url>
cd tasks

# 3. Install dependencies
uv sync

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your database credentials

# 5. Run migrations
uv run alembic upgrade head

# 6. Start the server
uv run uvicorn main:app --reload
```

Your API will be available at http://localhost:8000 🎉
