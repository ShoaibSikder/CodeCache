<p align="center"> <img src="frontend/public/favicon.svg" alt="logo" width="112" /> </p>

<h1 align="center">CodeCache</h1>

<p align="center"><strong>The fastest way to recall code.</strong><br />A learning and reference workspace for developers to browse programming topics, run code, get AI-assisted explanations, and track what they have learned.</p>

CodeCache combines a public learning site with a separately routed admin workspace. Learning content is organized as languages, sections, subsections, and individual content items, so explanations, code samples, notes, and warnings stay easy to browse and manage.

<p align="center">
  <img src="https://img.shields.io/badge/React-18-149eca?logo=react&logoColor=white" alt="React 18" />
  <img src="https://img.shields.io/badge/Django-5-092e20?logo=django&logoColor=white" alt="Django 5" />
  <img src="https://img.shields.io/badge/Database-Supabase-3ecf8e?logo=supabase&logoColor=white" alt="Supabase PostgreSQL" />
  <img src="https://img.shields.io/badge/License-not--specified-lightgrey" alt="No license specified" />
</p>

## Contents

- [Screenshots](#screenshots)
- [Core Features](#core-features)
- [Administration Features](#administration-features)
- [Role-Based Access](#role-based-access)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Backend Apps](#backend-apps)
- [Frontend Architecture](#frontend-architecture)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [API Overview](#api-overview)
- [Testing and Verification](#testing-and-verification)
- [Development Notes](#development-notes)
- [Deployment Notes](#deployment-notes)
- [Security Notes](#security-notes)
- [License](#license)

## Screenshots

Screenshots are stored in `frontend/public/system images/`.

| Screen | Preview |
|---|---|
| Home and language catalog | ![CodeCache home page](frontend/public/system%20images/home.png) |
| Sign in | ![CodeCache sign-in page](frontend/public/system%20images/login.png) |
| Registration | ![CodeCache registration page](frontend/public/system%20images/registration.png) |
| Code playground | ![CodeCache playground](frontend/public/system%20images/playground.png) |
| Administration | ![CodeCache admin panel](frontend/public/system%20images/admin%20panel.png) |

## Core Features

### Authentication and Accounts

- Register and sign in with an email address and password.
- Authenticate API requests with JSON Web Tokens (JWT), including access-token refresh and logout.
- View the signed-in user's profile.
- Protect saved snippets, learning progress, notes, and profile pages behind authentication.

### Learning Catalog

- Browse available programming languages from the home page.
- Open a language reference organized as **language → sections → subsections → content items**.
- Render learning material using typed content blocks: headings, paragraphs, code examples, tables, lists, notes, warnings, tips, output, images, and dividers.
- Copy and interact with code examples in the reference pages.
- Search learning material and retrieve search suggestions.

### Code Tools and AI

- Edit and run code in the playground, with optional standard input and a displayed execution result.
- Send execution requests through Django to the JDoodle API; provider credentials stay on the server.
- Ask the AI Code Doctor to review code and explain potential issues.
- Generate multiple-choice quizzes for a language or topic through the Groq API.

### Learning Progress

- Save and unsave reference content.
- Mark topics complete and review progress by language.
- View learning XP, activity streak, and learning overview.
- Keep personal language notes and return to the last language visited.

### Search and Activity

- Search the learning catalog and browse suggestions.
- Record page views and search activity for analytics.
- View popular content and aggregate usage statistics in the admin dashboard.

## Administration Features

The administration area has a dedicated layout and navigation.

### Content Management

- Manage programming languages.
- Create and update sections and subsections and organize them by display order.
- Create, update, and remove typed content items, including code and tables.
- Publish or change the status of catalog content.

### User and Usage Management

- Review registered accounts and manage user roles where the caller has super-administrator permission.
- View aggregate catalog, page-view, search, and popular-content analytics.

The backend independently checks the caller's role for protected operations; a page being visible in the frontend does not grant API access.

## Role-Based Access

| Role | Typical access |
|---|---|
| `user` | Public catalog and tools; authenticated personal learning features such as saved items, progress, and notes |
| `editor` | Limited editorial API access, including subsection management where allowed by backend permissions |
| `admin` | Admin workspace and protected language, section, content, and analytics operations |
| `super_admin` | Admin access plus protected user-management operations |

The browser routes are grouped as follows:

| Experience | Routes | Access |
|---|---|---|
| Public learning site | `/`, `/language/:slug`, `/search`, `/playground` | Public |
| Account | `/login`, `/register` | Public |
| Personal learning | `/saved`, `/learn`, `/profile` | Sign-in required |
| Administration | `/admin/login`, `/admin/dashboard`, `/admin/languages`, `/admin/sections`, `/admin/content`, `/admin/users` | Admin or super-admin role |

Frontend route guards are for user experience only. Django REST Framework permissions are the security boundary for API operations. Some API operations have narrower role requirements than the frontend admin route.

## Tech Stack

| Area | Implementation |
|---|---|
| Frontend | React 18, Vite 6, React Router 6 |
| Styling and UI | Tailwind CSS 3, Radix UI, Framer Motion, Lucide React, Sonner |
| Charts and API client | Recharts, Axios |
| Backend | Django 5.0, Django REST Framework, SimpleJWT |
| Database | Supabase-hosted PostgreSQL, accessed through Django ORM and psycopg |
| Media storage | Supabase Storage through a custom Django storage backend |
| AI | Groq API for Code Doctor and quiz generation |
| Code execution | JDoodle API, called by the Django backend |
| Production packages | Gunicorn; WhiteNoise is installed but not currently enabled as middleware |

The active persistence layer is the Django ORM with Supabase PostgreSQL. The backend requires a Supabase PostgreSQL `DATABASE_URL`; it does not fall back to SQLite. Prisma is listed as a historical project dependency but is not used by the current application runtime.

## Architecture

```text
CodeCache/
├── docs/
│   └── CodeCache Project Documentation.docx
├── backend/
│   ├── apps/
│   │   ├── accounts/       # Custom user model, registration, JWT and profile
│   │   ├── analytics/      # Page views, searches and usage statistics
│   │   ├── common/         # Shared models, role permissions and API helpers
│   │   ├── content/        # Sections, subsections and typed content items
│   │   ├── languages/      # Public catalog and admin language APIs
│   │   ├── learning/       # Completions, XP, saved items, notes and activity
│   │   ├── playground/     # JDoodle code execution integration
│   │   └── search/         # Catalog search and suggestions
│   ├── config/
│   │   └── settings/       # Shared, development and production settings
│   ├── utils/              # Supabase client and custom storage backend
│   ├── requirements/       # Base, development and production dependencies
│   ├── manage.py
│   └── .env.example
└── frontend/
    ├── public/             # Static assets and system screenshots
    ├── src/
    │   ├── components/     # Layout, code, learning and reusable UI
    │   ├── context/        # Authentication state
    │   ├── lib/            # Mock data, highlighting and shared helpers
    │   ├── pages/          # Public, account and admin pages
    │   └── services/       # API client and cache
    ├── package.json
    └── .env.example
```

The browser talks to the versioned Django REST API. Django connects to Supabase PostgreSQL and Supabase Storage; Groq and JDoodle credentials remain on the backend and are never required by the browser.

## Backend Apps

### `accounts`

Defines the custom user model, registration and login serializers, JWT token handling, profile/password operations, and super-admin user management.

### `languages`

Serves the public language catalog and complete language content trees. It also provides protected language-management endpoints and management commands for sample content.

### `content`

Models and APIs for sections, subsections, and content items. Content items use JSON data paired with a type such as `code`, `table`, `paragraph`, or `list`.

### `learning`

Stores authenticated users' topic completions, learning profiles, saved content, notes, and activity history.

### `search`

Provides public search across languages, sections, subsections, and content, plus search suggestions.

### `playground`

Validates and records code-execution requests, sends them to JDoodle, and returns normalized results.

### `analytics`

Tracks page views and searches, returns popular content, and supplies protected aggregate dashboard statistics.

### `common`

Contains shared UUID/timestamp model behavior, role constants and permissions, validators, pagination, and API error handling.

## Frontend Architecture

### `App.jsx`

Defines the public and authenticated routes and lazy-loads page modules. It also applies the client-side user/admin route guard.

### `context/AuthContext.jsx`

Loads the current profile, manages the access and refresh tokens, and exposes the authenticated user and role helpers to React components.

### `components/Layout.jsx` and `components/AdminLayout.jsx`

Provide separate public-site and admin layouts, headers, navigation, and responsive shells.

### `pages/`

Contains the home/catalog, language detail, search, playground, sign-in/registration, saved items, learning path, profile, and administration pages.

### `components/`

Contains reusable code cards/highlighting, typed learning-content rendering, learning challenges and tools, search, skeletons, and UI primitives.

### `services/`

Contains the Axios API client, JWT refresh handling, response normalization, and client-side request caching. `VITE_USE_MOCK=true` selects the built-in mock service instead of the Django API.

## Getting Started

### Prerequisites

- Python 3.10 or newer
- Node.js 18 or newer and npm
- A Supabase project with PostgreSQL; Supabase Storage is needed for media uploads.
- Groq API credentials to use live AI features.
- JDoodle API credentials to run code in the playground.

### 1. Configure Supabase

Create or select a Supabase project. Copy the PostgreSQL connection string from the project’s database connection settings and note the project URL and service-role key. Create the Storage bucket named in `SUPABASE_BUCKET` (the example uses `codecache-media`).

Use a PostgreSQL connection string with SSL enabled. Supabase pooler/direct connection options depend on the deployment environment; use the connection format recommended for that environment by Supabase.

### 2. Start the backend

From the repository root:

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements/base.txt
Copy-Item .env.example .env
```

Edit `backend/.env` and provide the Supabase, Groq, and JDoodle values described below. Then initialize the schema and start Django:

```powershell
python manage.py check
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The API runs at `http://localhost:8000`; the health endpoint is `http://localhost:8000/`. `createsuperuser` creates an active Django superuser and assigns the `super_admin` application role.

Groq and JDoodle credentials are optional for starting Django, but their respective AI and execution features will not work until configured. Supabase PostgreSQL credentials are required for the backend to start.

To seed the sample language catalog and learning content, run this optional command against the configured database:

```powershell
python manage.py seed_languages
```

> **Warning:** this command deletes and recreates the existing C course sections and content. For the other seeded languages, it deletes and recreates content items in seeded subsections. Back up the database and inspect `backend/apps/languages/management/commands/seed_languages.py` before running it against data you need to keep.

### 3. Start the frontend

In a second terminal from the repository root:

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```

Open the Vite URL printed in the terminal, usually `http://localhost:5173`. The frontend template points to `http://localhost:8000/api/v1` and disables mock mode by default. The backend development settings allow local frontend origins.

For macOS/Linux, activate the virtual environment with `source .venv/bin/activate` and copy environment templates with `cp .env.example .env`. The backend setup commands above are written for PowerShell.

## Environment Variables

The repository includes templates at `backend/.env.example` and `frontend/.env.example`. Keep actual credentials in local, untracked `.env` files or your deployment secret manager.

### Backend

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Django secret key; use a strong unique value outside local development |
| `DEBUG` | Django debug mode; disable in production |
| `ALLOWED_HOSTS` | Comma-separated backend hostnames |
| `DATABASE_URL` | Supabase PostgreSQL connection URL |
| `SUPABASE_URL` | Supabase project URL |
| `SUPABASE_SERVICE_KEY` | Server-side service-role key for Storage operations; keep secret |
| `SUPABASE_BUCKET` | Storage bucket used for uploaded media |
| `GROQ_API_KEY` | Groq API key for AI features |
| `GROQ_MODEL` | Groq model identifier |
| `JDOODLE_CLIENT_ID` | JDoodle application client ID |
| `JDOODLE_CLIENT_SECRET` | JDoodle application secret |
| `JDOODLE_API_URL` | JDoodle execution API URL |
| `JDOODLE_VERSION_INDEX` | JDoodle language-version index setting |
| `CORS_ALLOWED_ORIGINS` | Comma-separated frontend origins in production settings |
| `FRONTEND_URL` | Present in the template, but not currently read by Django settings |

### Frontend

| Variable | Purpose |
|---|---|
| `VITE_API_URL` | Django API origin or base URL; the client appends `/api/v1` if needed |
| `VITE_USE_MOCK` | Set to `true` only to use the frontend mock API instead of Django |

Never put Supabase service-role, Groq, or JDoodle secrets in a `VITE_` variable: values with that prefix are bundled into browser code.

`DATABASE_URL` is required even for a Django system check. It must use PostgreSQL and point to a Supabase host; the backend enforces SSL and does not provide a local SQLite fallback. The development settings currently allow all CORS origins; production uses `CORS_ALLOWED_ORIGINS`.

## API Overview

All application endpoints are under `/api/v1/` unless noted.

| Area | Methods and endpoints | Purpose |
|---|---|---|
| Health | `GET /`, `GET /warmup/` | Service health and warmup responses |
| Authentication | `POST /auth/register/`, `/auth/login/`, `/auth/refresh/`, `/auth/logout/`; `GET /auth/profile/`; `POST /auth/password-change/` | Registration, JWT session, profile, and password operations |
| Users | `GET /auth/users/`, `PATCH /auth/users/<id>/` | Protected user administration |
| Public catalog | `GET /languages/`, `GET /languages/<slug>/` | List languages and fetch a language's content tree |
| Language administration | `/admin/languages/`, `/admin/languages/<id>/` | Protected language CRUD |
| Sections | `/admin/sections/`, `/admin/sections/<id>/` | Protected section CRUD |
| Subsections | `/admin/subsections/`, `/admin/subsections/<id>/` | Protected subsection CRUD |
| Content items | `/admin/content-items/`, `/admin/content-items/<id>/` | Protected content-item CRUD |
| Search | `GET /search/?q=<query>`, `GET /search/suggestions/?q=<query>` | Search the catalog and request suggestions |
| Learning | `/learning/overview/`, `/learning/topics/<subsection-id>/complete/`, `/learning/saved/`, `/learning/notes/<language>/`, `/learning/activities/`, `/learning/last-language/` | Authenticated learning progress and personal content |
| Playground | `GET /playground/languages/`, `POST /playground/run/` | List supported runtimes and run code through JDoodle |
| AI | `POST /ai/code-doctor/`, `POST /ai/generate-quiz/` | Code analysis and quiz generation through Groq |
| Analytics | `/analytics/`, `/analytics/view/`, `/analytics/search/`, `/analytics/popular/` | Dashboard statistics, event tracking, and popular content |

Endpoints that read or modify personal learning data require JWT authentication. Administrative endpoints also apply backend role permissions. Django's built-in administration is available at `/admin/`.

## Testing and Verification

From `backend/`, with the backend virtual environment active, run Django checks and tests:

```powershell
python manage.py check
python manage.py test
```

The Django tests currently cover selected Supabase Storage and playground behavior in `apps/languages/tests.py` and `apps/playground/tests.py`. Install the optional developer tools with `pip install -r requirements/development.txt` if using pytest or the configured lint/format tools.

From `frontend/`, build the production bundle:

```powershell
npm run build
```

The frontend build writes deployable static files to `frontend/dist/`. There is no `test` script in the current frontend `package.json`.

## Deployment Notes

- Deploy the Django backend with `config.settings.production`, a production WSGI server such as Gunicorn, and the required environment variables. Set `DJANGO_SETTINGS_MODULE=config.settings.production` in the backend environment.
- Set strong production secrets and explicit `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS` values. Configure HTTPS and the Supabase PostgreSQL connection for the production environment.
- The production settings write logs to `backend/logs/codecache.log`; create that directory with suitable write permissions or change the logging configuration before deployment.
- WhiteNoise is included in the requirements, but its middleware is not enabled in the current shared middleware list. Configure static-file serving for the deployment rather than assuming it is active.
- Build the frontend with `npm run build` and serve `frontend/dist/` from a static hosting provider.
- Set the production `VITE_API_URL` at build time to the deployed API base URL ending in `/api/v1`.
- Configure platform health checks against `GET /` and ensure the Supabase Storage bucket and policies match the application’s upload/public-read behavior.

## Security Notes

- Keep `.env` files and all service credentials out of version control.
- `SUPABASE_SERVICE_KEY` is privileged and must only be used by the backend.
- AI and compiler API calls are proxied by Django so provider credentials are not exposed to users.
- Use HTTPS, production Django settings, restricted CORS origins, and strong secrets in deployed environments.
- Apply authorization at the API level; hiding an admin route in the frontend does not protect backend data.

## Development Notes

- The API uses versioned paths under `/api/v1/`; the frontend normalizes `VITE_API_URL` and appends that prefix if it is not already present.
- The built-in mock API can be enabled locally with `VITE_USE_MOCK=true`; the default is to use Django.
- The `seed_languages` command is destructive for existing C course sections and for content in seeded subsections. Do not use it as a harmless one-time setup step on a populated database.
- The backend has targeted Django tests for Supabase Storage and the JDoodle playground. The frontend package currently provides a production build script but no dedicated test script.
- No `LICENSE` file is present in the repository; confirm licensing before redistributing the project.

## License

No license is currently specified in the repository. Until a license is added, do not assume the code is available for reuse or redistribution.

---

Created by [@shoaibsikder](https://shoaibsikderportfolio.vercel.app) to make programming concepts easier to explore, practice, and remember.
