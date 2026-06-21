# CodeCache

A modern, AI-powered code snippet reference platform for developers. Features include editable code snippets, an AI Code Doctor powered by Groq, knowledge quizzes, and an admin dashboard.

## Stack

- **Frontend**: React 18 + Vite + Tailwind CSS + shadcn/ui
- **Backend**: Django + Django REST Framework
- **Database**: Supabase PostgreSQL + Prisma ORM
- **Storage**: Supabase Storage Bucket
- **AI**: Groq API (Llama 3.3 70B)

## Project Structure

```
CodeCache/
  frontend/          # React frontend (JSX)
    src/
      components/    # UI components & feature components
      pages/         # Home, LanguagePage, AdminDashboard
      services/      # API layer (axios)
      hooks/         # Custom React hooks
      lib/           # Utilities
  backend/           # Django DRF backend
    apps/            # Django apps
    config/          # Django settings
    utils/           # Prisma & Supabase clients
    schema.prisma    # Prisma schema
```

## Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 18+
- Supabase account
- Groq API key

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd CodeCache
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements/base.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials:
# - DATABASE_URL (Supabase PostgreSQL connection string)
# - SUPABASE_URL & SUPABASE_SERVICE_KEY
# - GROQ_API_KEY
# - SECRET_KEY

# Generate Prisma client
prisma generate

# Run migrations (creates tables in Supabase)
prisma migrate dev --name init

# Or use Django migrations for auth tables
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set environment variables
cp .env .env.local
# Edit .env.local with your API URL:
# VITE_API_URL=http://localhost:8000

# Run development server
npm run dev
```

### 4. Production Build

```bash
cd frontend
npm run build

# Deploy dist/ folder to Vercel
cd backend
# Deploy to Render (use gunicorn)
```

## Environment Variables

### Backend (.env)

```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Supabase PostgreSQL
DATABASE_URL=postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres

# Supabase Storage
SUPABASE_URL=https://[project-ref].supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key
SUPABASE_BUCKET=codecache-media

# Groq AI
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama-3.3-70b-versatile
```

### Frontend (.env)

```
VITE_API_URL=http://localhost:8000
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/` | GET | Health check |
| `/api/v1/auth/register/` | POST | Register new user |
| `/api/v1/auth/login/` | POST | Login and get JWT |
| `/api/v1/auth/profile/` | GET | Get user profile |
| `/api/v1/auth/users/` | GET | List all users (admin) |
| `/api/v1/languages/` | GET | List all languages |
| `/api/v1/languages/<slug>/` | GET | Language detail with sections |
| `/api/v1/ai/code-doctor/` | POST | AI code analysis |
| `/api/v1/search/?q=query` | GET | Full-text search |
| `/api/v1/playground/run/` | POST | Execute code via Judge0 |
| `/api/v1/admin/languages/` | CRUD | Admin language management |
| `/api/v1/admin/sections/` | CRUD | Admin section management |
| `/api/v1/admin/subsections/` | CRUD | Admin subsection management |
| `/api/v1/admin/content-items/` | CRUD | Admin content item management |

## Features

- **Code Snippets**: Browse, copy, edit, and run code snippets
- **AI Code Doctor**: Get AI-powered code analysis and fixes via Groq
- **Knowledge Quizzes**: Test your understanding with interactive quizzes
- **Syntax Highlighting**: Beautiful code display with line numbers
- **Dark Mode**: Toggle between light and dark themes
- **Admin Dashboard**: Manage languages, sections, and content
- **Responsive Design**: Works on all devices and screen sizes
- **Loading Skeletons**: Smooth loading experience

## Deployment

### Frontend (Vercel)

1. Push code to GitHub
2. Import project in Vercel
3. Set build command: `npm run build`
4. Set output directory: `dist`
5. Add environment variable: `VITE_API_URL`

### Backend (Render)

1. Push code to GitHub
2. Create new Web Service in Render
3. Set build command: `pip install -r requirements/base.txt`
4. Set start command: `gunicorn config.wsgi:application`
5. Add all environment variables from `.env.example`

## License

Built by [@shoaibsikder](https://shoaibsikderportfolio.vercel.app)
