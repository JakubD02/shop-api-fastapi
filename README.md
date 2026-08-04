# Simple Shop API

RESTful API for product management. Learning project built with FastAPI, SQLAlchemy 2.0, and Pydantic v2, containerized with Docker.

## Features

- Full CRUD operations for products
- Filtering by category, price range, and active status
- Dynamic sorting (by id, name, price, stock, created_at) with ascending/descending order
- Pagination (skip/limit)
- Auto-generated Swagger UI documentation
- Enum-based product categories with type safety
- Containerized with Docker for consistent deployment
- Automated code linting and formatting with Ruff (via GitHub Actions)

## Tech Stack

- **Python** 3.13
- **FastAPI** - modern async web framework
- **SQLAlchemy** 2.0 - ORM
- **Pydantic** v2 - data validation
- **SQLite** - database (development)
- **Uvicorn** - ASGI server
- **Docker** & **Docker Compose** - containerization
- **Ruff** - linter and code formatter
- **GitHub Actions** - CI/CD pipeline

## Project Structure

    shopping/
    ├── .github/
    │   └── workflows/
    │       └── ruff.yml         # GitHub Actions workflow for linting
    ├── main.py                  # FastAPI app and endpoints
    ├── database.py              # Engine, SessionLocal, get_db dependency
    ├── models.py                # SQLAlchemy Product model
    ├── schemas.py               # Pydantic schemas (Create/Update/Read)
    ├── enums.py                 # ProductCategory enum
    ├── requirements.txt         # Python dependencies
    ├── Dockerfile               # Container definition
    ├── docker-compose.yml       # Multi-container orchestration with live reload
    ├── ruff.toml                # Ruff configuration
    ├── .gitignore
    └── shop.db                  # SQLite database (auto-created, not committed)

## Setup

### Local Development

```bash
git clone https://github.com/JakubD02/shop-api-fastapi.git
cd shop-api-fastapi
python -m venv venv
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

Open Swagger UI: `http://localhost:8000/docs`

### Docker

Simple run:

```bash
docker build -t shop-api .
docker run -p 8000:8000 shop-api
```

With Docker Compose (live reload):

```bash
docker-compose up
```

Then open `http://localhost:8000/docs`.

## Code Quality

Format and lint code with Ruff:

```bash
ruff format .
ruff check . --fix
```

All pushes to `main` are automatically checked via GitHub Actions.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root |
| POST | `/products/` | Create a new product |
| GET | `/products/` | List products (with filtering, sorting, pagination) |
| GET | `/products/{product_id}/` | Get product by ID |
| PATCH | `/products/{product_id}/` | Update product (partial) |
| DELETE | `/products/{product_id}/` | Delete product |

## Query Parameters — List Products

`GET /products/` supports:

- `category` — filter by category (electronics, books, clothing, food, sport, tools, other)
- `min_price` / `max_price` — filter by price range
- `is_active` — filter by active status
- `sort_by` — `id`, `name`, `price`, `stock`, `created_at` (default: `id`)
- `order` — `asc` or `desc` (default: `asc`)
- `skip` / `limit` — pagination (default: 0 / 5, max: 100)

**Example:** `GET /products/?category=electronics&min_price=100&sort_by=price&order=desc&limit=10`
