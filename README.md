# Discord Clone

A real-time chat application inspired by Discord, built with **Svelte** for the frontend and **FastAPI** for the backend.

---

## Features

- Real-time messaging
- Multiple channels and direct messages
- User authentication
- Responsive UI

---

## Tech Stack

- **Frontend:** Svelte, JavaScript, TailwindCSS
- **Backend:** Python, FastAPI
- **Database:** PostgreSQL
- **Websockets:** For real-time messaging
- **Other:** JWT for authentication

---

## Prerequisites

- Node.js (v16+)
- npm
- Python 3.9+
- pip
- PostgreSQL

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/discord-clone.git
cd discord-clone
```

### 2. Backend Setup
Install dependencies
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
pip install -r requirements.txt
```

Set environment variables:
```
JWT_SECRET_KEY="__insert_token_here__"
DB_USER="__insert_database_username_here__"
DB_PASSWORD="__insert_database_password_here__"
DB_HOST="__insert_database_adress_here__"
DB_NAME="__insert_database_name_here__"
```

Start the server:
```bash
python ./main.py
```

### 3. Frontend Setup
Install dependencies
```bash
cd frontend
npm install
```

Start the development server:
```bash
npm run dev
```
