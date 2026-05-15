# AI Partner

An AI companion chat community platform. Users can create and customize AI virtual characters, browse public characters, follow them, and chat with them.

## Tech Stack

- **Frontend**: Vue 3 + TypeScript + Naive UI + Pinia + Vue Router
- **Backend**: Django + Django REST Framework + SimpleJWT
- **Database**: SQLite (development), migratable to MySQL

## Prerequisites

- Python 3.10+
- Node.js 18+

## Quick Start

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver     # Runs at http://localhost:8000 by default
```

### Frontend

```bash
cd frontend
npm install
npm run dev                     # Runs at http://localhost:5173 by default
```

### Model Configuration

Visit `http://localhost:8000/admin/` and log in with the superuser account. Add LLM model configs under Model Configs:

- **provider**: Service provider, e.g. openai, deepseek
- **model_name**: Model name, e.g. gpt-4o, deepseek-chat
- **api_key**: API key
- **api_base_url**: API endpoint URL (leave blank for OpenAI official API; fill in for compatible services, e.g. `https://api.deepseek.com/v1`)

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
