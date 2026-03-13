# ⏳ Chrono Temporal API Framework

[![PyPI version](https://badge.fury.io/py/chrono-temporal.svg)](https://pypi.org/project/chrono-temporal/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

A powerful backend framework that gives any data entity **time-travel superpowers**. Query what your data looked like at any point in history, track full change histories, and diff any two points in time — all through a clean REST API.

---

## 🚀 The Problem

Most databases only store the **current state** of data. When something changes, the old version is gone forever. This causes real pain:

- _"What was this user's subscription plan when they made this purchase?"_ — you can't know
- Audit trails and compliance become a nightmare
- Debugging production issues that depended on state that no longer exists

Developers hack around this with `created_at`/`updated_at` columns and manual audit tables — all bespoke, inconsistent, and painful to query.

---

## ✅ The Solution

Chrono gives every entity a **time dimension**. Store any entity with a validity period and query it across time with zero extra effort.

---

## ✨ Features

- 🕐 **Time-travel queries** — Get the exact state of any entity at any point in history
- 📜 **Full history** — See the complete timeline of changes for any entity
- 🔍 **Diff engine** — Compare any two points in time and see exactly what changed
- 🔐 **API key authentication** — Secure your API with generated keys
- 📦 **Generic** — Works with any entity type (users, orders, products, contracts — anything)
- ⚡ **Async** — Built with FastAPI and async SQLAlchemy for high performance
- 🐳 **Docker ready** — Run the full stack with one command
- 📖 **Auto docs** — Interactive Swagger UI out of the box

---

## 📦 Install the Python Package

Just want the core library? Install it directly:

```bash
pip install chrono-temporal
```

```python
from chrono_temporal import TemporalService, TemporalRecordCreate, get_engine, get_session, create_tables
from datetime import datetime, timezone

engine = get_engine("postgresql+asyncpg://user:pass@localhost/mydb")
session_factory = get_session(engine)

async with session_factory() as session:
    svc = TemporalService(session)

    # Time-travel query
    records = await svc.get_at_point_in_time(
        "user", "user_001", datetime(2024, 3, 1, tzinfo=timezone.utc)
    )

    # Diff between two dates
    diff = await svc.get_diff(
        "user", "user_001",
        datetime(2024, 1, 1, tzinfo=timezone.utc),
        datetime(2025, 7, 1, tzinfo=timezone.utc),
    )
    print(diff["changed"])  # {"plan": {"from": "free", "to": "pro"}}
```

👉 [View on PyPI](https://pypi.org/project/chrono-temporal/)

---

## 🛠 Tech Stack

| Tool               | Purpose                           |
| ------------------ | --------------------------------- |
| **FastAPI**        | Modern async Python web framework |
| **PostgreSQL**     | Battle-tested relational database |
| **SQLAlchemy 2.0** | Async ORM                         |
| **Alembic**        | Database migrations               |
| **Pydantic**       | Data validation                   |
| **asyncpg**        | Async PostgreSQL driver           |
| **Docker**         | Containerized deployment          |

---

## 🐳 Quick Start with Docker

The fastest way to run the full API — no setup required:

```bash
# Clone the repo
git clone https://github.com/Daniel7303/chrono-temporal-api-framework.git
cd chrono-temporal-api-framework

# Create your environment file
cp .env.docker.example .env.docker

# Start everything
docker-compose up --build
```

Visit `http://localhost:8000/docs` for the interactive API docs. ✅

---

## 🖥️ Manual Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 15+

### Installation

```bash
# Clone the repo
git clone https://github.com/Daniel7303/chrono-temporal-api-framework.git
cd chrono-temporal-api-framework

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### Configure environment

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql+asyncpg://postgres:yourpassword@localhost:5432/temporal_api
DATABASE_URL_SYNC=postgresql+psycopg2://postgres:yourpassword@localhost:5432/temporal_api
APP_NAME=Chrono Temporal API Framework
APP_VERSION=0.1.0
DEBUG=True
```

### Run the server

```bash
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for the interactive API docs.

---

## 🔌 API Endpoints

### Framework

| Method  | Endpoint                                      | Description              |
| ------- | --------------------------------------------- | ------------------------ |
| `POST`  | `/api/v1/temporal/`                           | Create a temporal record |
| `GET`   | `/api/v1/temporal/{id}`                       | Get a record by ID       |
| `GET`   | `/api/v1/temporal/entity/{type}/{id}/current` | Get current state        |
| `GET`   | `/api/v1/temporal/entity/{type}/{id}/history` | Get full history         |
| `GET`   | `/api/v1/temporal/entity/{type}/{id}/as-of`   | Time-travel query        |
| `GET`   | `/api/v1/temporal/entity/{type}/{id}/diff`    | Diff two points in time  |
| `PATCH` | `/api/v1/temporal/{id}/close`                 | Close a record           |

### Authentication

| Method   | Endpoint          | Description            |
| -------- | ----------------- | ---------------------- |
| `POST`   | `/auth/keys/`     | Generate a new API key |
| `GET`    | `/auth/keys/`     | List all API keys      |
| `DELETE` | `/auth/keys/{id}` | Revoke an API key      |

### Demo — Subscription Management

| Method  | Endpoint                                     | Description                    |
| ------- | -------------------------------------------- | ------------------------------ |
| `POST`  | `/demo/subscriptions/customers`              | Create a customer              |
| `GET`   | `/demo/subscriptions/customers/{id}`         | Get current state              |
| `PATCH` | `/demo/subscriptions/customers/{id}/plan`    | Upgrade/downgrade plan         |
| `GET`   | `/demo/subscriptions/customers/{id}/history` | Full plan history              |
| `GET`   | `/demo/subscriptions/customers/{id}/as-of`   | Plan at a point in time        |
| `GET`   | `/demo/subscriptions/customers/{id}/diff`    | What changed between two dates |

---

## 💡 Example Usage

### 1. Generate an API key

```bash
POST /auth/keys/
{ "name": "my-app" }

# Returns (shown only once — store it!)
{ "raw_key": "chron_sk_a1b2c3..." }
```

### 2. Create a temporal record

```bash
POST /api/v1/temporal/
X-API-Key: chron_sk_a1b2c3...

{
  "entity_type": "user",
  "entity_id": "user_001",
  "valid_from": "2024-01-01T00:00:00Z",
  "data": { "name": "Daniel", "plan": "free" }
}
```

### 3. Time-travel query

```bash
GET /api/v1/temporal/entity/user/user_001/as-of?as_of=2024-03-01T00:00:00Z
X-API-Key: chron_sk_a1b2c3...

# Returns the state of user_001 on March 1st 2024
```

### 4. Diff between two dates

```bash
GET /api/v1/temporal/entity/user/user_001/diff?from_dt=2024-01-01T00:00:00Z&to_dt=2025-07-01T00:00:00Z
X-API-Key: chron_sk_a1b2c3...

# Returns:
{
  "changed": { "plan": { "from": "free", "to": "pro" } },
  "unchanged": ["name", "email"],
  "has_changes": true
}
```

---

## 🗺 Roadmap

- [x] Core temporal framework
- [x] Time-travel queries
- [x] Diff engine
- [x] API key authentication
- [x] Subscription management demo
- [x] Docker support
- [x] PyPI package (`pip install chrono-temporal`)
- [ ] Deploy to cloud (DigitalOcean / Railway)
- [ ] Stripe payments for hosted API
- [ ] Timeline visualization dashboard

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

---

## 📄 License

MIT License — free to use, modify, and distribute.
