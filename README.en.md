# AI Partner

An AI companion chat community platform. Users can create and customize AI virtual characters, browse public characters, follow them, and chat with them.

## Tech Stack

- **Frontend**: Vue 3 + TypeScript + Naive UI + Pinia + Vue Router
- **Backend**: Django + Django REST Framework + SimpleJWT
- **Database**: SQLite (development), migratable to MySQL

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Model Configuration

Visit `http://localhost:8000/admin/` and log in with the superuser account. Add LLM model configs under Model Configs (provider, model_name, api_key).

## Pages

| Page | Route | Description |
|------|-------|-------------|
| Square | `/` | Browse public AI characters, search, sort, and filter |
| Chat | `/chat/:id` | Real-time streaming chat with AI characters |
| Friends | `/friends` | Recent chats and followed AI characters |
| Create | `/create` | Create and manage AI characters |
| Profile | `/profile` | Profile and avatar management |

---

[:cn: 中文版本](./README.md)
