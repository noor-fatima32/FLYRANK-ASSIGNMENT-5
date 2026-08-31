# FlyRank — Auth Login & Protect

A FastAPI authentication API built with **Supabase Auth** and **JWT-based protected routes**.

This project demonstrates user signup, login, JWT authentication, protected API endpoints, reusable authentication dependencies, dashboard access, logout, and Swagger Bearer authentication.

---

## Features

- User signup with email and password
- User login with email and password
- Supabase Auth integration
- JWT access token generation
- Public endpoint
- Protected endpoint
- JWT verification
- Invalid/expired token rejection
- Reusable authentication dependency
- Protected dashboard endpoint
- Logout endpoint
- Swagger/OpenAPI documentation
- Swagger Bearer authentication
- Environment variable configuration
- Secure `.env` handling
- Git-friendly project structure

---

# Tech Stack

- **Python 3**
- **FastAPI**
- **Uvicorn**
- **Supabase**
- **Supabase Auth**
- **JWT**
- **Pydantic**
- **python-dotenv**

---

# Project Structure

```text
auth-login-protect/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### Local-only file

```text
.env
```

The `.env` file contains local Supabase credentials and must **never** be committed to Git.

---

# Requirements

Make sure the following are installed:

- Python 3
- Git
- A Supabase account
- A Supabase project

Check Python:

```powershell
python --version
```

Check Git:

```powershell
git --version
```

---

# 1. Clone the Repository

```powershell
git clone YOUR_GITHUB_REPOSITORY_URL
```

Enter the project:

```powershell
cd auth-login-protect
```

---

# 2. Create Virtual Environment

On Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

You should see:

```text
(.venv)
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then activate again:

```powershell
.venv\Scripts\Activate.ps1
```

---

# 3. Install Dependencies

Install the project dependencies:

```powershell
pip install -r requirements.txt
```

If `requirements.txt` does not exist, install manually:

```powershell
pip install fastapi "uvicorn[standard]" supabase python-dotenv
```

Then generate the requirements file:

```powershell
pip freeze > requirements.txt
```

---

# 4. Configure Supabase

Create a Supabase project.

From the Supabase dashboard, obtain:

- Project URL
- Publishable/anonymous API key

The application expects these values in environment variables.

---

# 5. Configure Supabase Email Authentication

In Supabase:

```text
Authentication
    ↓
Providers
    ↓
Email
```

Enable email/password authentication.

For this assignment/demo, email confirmation can be disabled so a newly registered test user can log in immediately.

---

# 6. Create `.env`

Create a `.env` file in the project root:

```powershell
notepad .env
```

Add:

```env
SUPABASE_URL=https://YOUR_PROJECT_REF.supabase.co
SUPABASE_KEY=YOUR_SUPABASE_PUBLISHABLE_KEY
PORT=8000
```

Replace the placeholder values with your actual Supabase project information.

### Example

```env
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_KEY=sb_publishable_xxxxxxxxxxxxxxxxx
PORT=8000
```

**Never commit the real `.env` file.**

---

# 7. `.env.example`

The repository contains `.env.example` so other developers know which variables are required.

Example:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_publishable_key
PORT=8000
```

Copy it to create your local environment file if needed:

```powershell
Copy-Item .env.example .env
```

Then edit:

```powershell
notepad .env
```

---

# 8. Start the API

Run:

```powershell
uvicorn app:app --reload
```

Expected:

```text
Uvicorn running on http://127.0.0.1:8000
```

Keep this terminal running.

---

# 9. API Documentation

FastAPI automatically provides Swagger UI.

Open:

```text
http://127.0.0.1:8000/docs
```

You can test all API endpoints directly from Swagger.

OpenAPI JSON is available at:

```text
http://127.0.0.1:8000/openapi.json
```

---

# API Endpoints

| Method | Endpoint | Authentication |
|---|---|---|
| GET | `/health` | Public |
| POST | `/auth/signup` | Public |
| POST | `/auth/login` | Public |
| GET | `/public` | Public |
| GET | `/protected` | JWT required |
| GET | `/dashboard` | JWT required |
| POST | `/auth/logout` | JWT required |

---

# Testing

The following commands are written for **Windows PowerShell**.

---

## Test 1 — Health Check

Open a second PowerShell terminal.

Navigate to the project:

```powershell
cd "C:\Users\fruit\Desktop\FlyRank\Assignment #5\auth-login-protect"
```

Activate the environment:

```powershell
.venv\Scripts\Activate.ps1
```

Run:

```powershell
curl.exe -i http://127.0.0.1:8000/health
```

Expected:

```text
HTTP/1.1 200 OK
```

Response:

```json
{
  "status": "ok",
  "message": "Server running and connected to Supabase"
}
```

---

# Test 2 — Public Endpoint

Run:

```powershell
curl.exe -i http://127.0.0.1:8000/public
```

Expected:

```text
HTTP/1.1 200 OK
```

Response:

```json
{
  "message": "This is a public endpoint"
}
```

No JWT is required.

---

# Test 3 — Signup

Use `Invoke-RestMethod` on Windows PowerShell because it avoids JSON quoting problems that can occur with `curl.exe`.

Create the request body:

```powershell
$body = @{
    email = "testuser@example.com"
    password = "TestPassword123!"
} | ConvertTo-Json
```

Send the signup request:

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/auth/signup" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

Expected response:

```text
message        : Signup successful
user_id        : ...
email          : testuser@example.com
```

If the email already exists, use another test email:

```text
testuser2@example.com
```

---

# Test 4 — Login

Create the login request:

```powershell
$body = @{
    email = "testuser@example.com"
    password = "TestPassword123!"
} | ConvertTo-Json
```

Send it:

```powershell
$login = Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/auth/login" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

Display the response:

```powershell
$login
```

Expected:

```text
message       : Login successful
access_token  : eyJ...
token_type    : bearer
user_id       : ...
email         : testuser@example.com
```

---

# Test 5 — Store the JWT

Store the JWT in a PowerShell variable:

```powershell
$TOKEN = $login.access_token
```

Verify that a token exists without printing the complete token:

```powershell
$TOKEN.Length
```

The result should be greater than:

```text
0
```

You can safely inspect only the first few characters:

```powershell
$TOKEN.Substring(0,10)
```

A JWT normally begins with something similar to:

```text
eyJhbGciOi
```

**Never publish or commit the complete token.**

---

# Test 6 — Protected Endpoint Without Token

Run:

```powershell
curl.exe -i http://127.0.0.1:8000/protected
```

Expected:

```text
HTTP/1.1 403 Forbidden
```

This demonstrates that the protected endpoint cannot be accessed without authentication.

---

# Test 7 — Protected Endpoint With Valid JWT

Create the Authorization header:

```powershell
$headers = @{
    Authorization = "Bearer $TOKEN"
}
```

Send the request:

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/protected" `
    -Method Get `
    -Headers $headers
```

Expected:

```text
message : You have access to the protected endpoint
user_id : ...
email   : testuser@example.com
```

This confirms:

```text
JWT
 ↓
Authorization Header
 ↓
FastAPI
 ↓
Supabase JWT Verification
 ↓
Protected Resource
```

---

# Test 8 — Invalid JWT

Create a fake token:

```powershell
$badHeaders = @{
    Authorization = "Bearer this-is-not-a-real-jwt"
}
```

Send:

```powershell
try {
    Invoke-RestMethod `
        -Uri "http://127.0.0.1:8000/protected" `
        -Method Get `
        -Headers $badHeaders
}
catch {
    $_.ErrorDetails.Message
}
```

Expected:

```json
{
  "detail": "Invalid or expired token"
}
```

This confirms invalid JWTs are rejected.

---

# Test 9 — Dashboard Without Token

Run:

```powershell
curl.exe -i http://127.0.0.1:8000/dashboard
```

Expected:

```text
HTTP/1.1 403 Forbidden
```

---

# Test 10 — Dashboard With Valid JWT

Make sure:

```powershell
$headers = @{
    Authorization = "Bearer $TOKEN"
}
```

Then:

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/dashboard" `
    -Method Get `
    -Headers $headers
```

Expected:

```text
message : Welcome to your dashboard
user_id : ...
email   : testuser@example.com
```

---

# Test 11 — Logout

With the authenticated headers:

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/auth/logout" `
    -Method Post `
    -Headers $headers
```

Expected:

```text
message : Logout successful
user_id : ...
```

The endpoint requires an authenticated request.

---

# Test 12 — Swagger Bearer Authentication

Open:

```text
http://127.0.0.1:8000/docs
```

Find the:

```text
Authorize
```

button.

Click it.

Enter the JWT access token obtained from:

```text
POST /auth/login
```

With FastAPI `HTTPBearer`, Swagger handles the Bearer authentication scheme.

Click:

```text
Authorize
```

Then:

```text
Close
```

Now test:

```text
GET /protected
```

Click:

```text
Try it out
```

Then:

```text
Execute
```

Expected response:

```json
{
  "message": "You have access to the protected endpoint",
  "user_id": "...",
  "email": "testuser@example.com"
}
```

Also test:

```text
GET /dashboard
```

and:

```text
POST /auth/logout
```

---

# Authentication Flow

```text
                    ┌─────────────────┐
                    │      User       │
                    └────────┬────────┘
                             │
                    POST /auth/signup
                             │
                             ▼
                    ┌─────────────────┐
                    │  Supabase Auth  │
                    └────────┬────────┘
                             │
                         Account
                             │
                             ▼
                    POST /auth/login
                             │
                             ▼
                    ┌─────────────────┐
                    │  Supabase Auth  │
                    └────────┬────────┘
                             │
                         JWT Token
                             │
                             ▼
                    Authorization Header
                             │
                             ▼
                    ┌─────────────────┐
                    │    FastAPI      │
                    └────────┬────────┘
                             │
                    get_current_user()
                             │
                             ▼
                    Supabase JWT Check
                             │
                    ┌────────┴────────┐
                    │                 │
                  Valid             Invalid
                    │                 │
                    ▼                 ▼
              Protected          HTTP 401
               Resource
```

---

# Reusable Authentication Dependency

Protected routes use the reusable:

```python
get_current_user()
```

dependency.

Example:

```python
@app.get("/protected")
def protected(current_user=Depends(get_current_user)):
    ...
```

The dashboard also uses the same dependency:

```python
@app.get("/dashboard")
def dashboard(current_user=Depends(get_current_user)):
    ...
```

This avoids duplicating authentication logic across protected routes.

---

# Security

## Environment Variables

Sensitive configuration is stored in:

```text
.env
```

The `.env` file is ignored by Git.

The repository contains:

```text
.env.example
```

instead.

---

## `.gitignore`

The project ignores:

```text
.venv/
__pycache__/
*.pyc
.env
```

---

## Never Commit

Never commit:

```text
.env
```

Never commit:

- Supabase secret keys
- Supabase service-role keys
- Passwords
- JWT access tokens
- Other private credentials

---

# Verify `.env` Is Not Tracked

Run:

```powershell
git ls-files .env
```

Expected:

```text
```

There should be **no output**.

Verify that `.env` still exists locally:

```powershell
Test-Path .env
```

Expected:

```text
True
```

This means:

- `.env` exists on your computer
- `.env` is not tracked by Git

---

# Git Workflow

Check status:

```powershell
git status
```

Add changes:

```powershell
git add .
```

Commit:

```powershell
git commit -m "Stage 6: finalize documentation and project cleanup"
```

View commit history:

```powershell
git log --oneline
```

Push to GitHub:

```powershell
git push origin main
```

---

# Stage Commit History

The project was developed incrementally:

```text
Stage 0: setup server and Supabase client
Stage 1: add signup and login
Stage 2: add protected routes and JWT verification
Stage 3: verify Supabase JWT tokens
Stage 4: add reusable auth dependency and dashboard
Stage 5: enable Swagger bearer authentication
Stage 6: finalize documentation and project cleanup
```

---

# Troubleshooting

## Error: Email signups are disabled

If signup returns:

```text
Email signups are disabled
```

Go to Supabase:

```text
Authentication
→ Providers
→ Email
```

Enable email/password signup.

---

## Error: JSON decode error

If `curl.exe` produces:

```text
JSON decode error
```

Use PowerShell's:

```powershell
Invoke-RestMethod
```

instead.

Example:

```powershell
$body = @{
    email = "testuser@example.com"
    password = "TestPassword123!"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/auth/signup" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

---

## Error: Not authenticated

If `/protected` returns:

```json
{
  "detail": "Not authenticated"
}
```

Make sure the JWT is stored:

```powershell
$TOKEN.Length
```

It should be greater than zero.

Then recreate the headers:

```powershell
$headers = @{
    Authorization = "Bearer $TOKEN"
}
```

Then retry:

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/protected" `
    -Method Get `
    -Headers $headers
```

---

## Error: Invalid or expired token

If you receive:

```json
{
  "detail": "Invalid or expired token"
}
```

Login again and obtain a fresh JWT:

```powershell
$body = @{
    email = "testuser@example.com"
    password = "TestPassword123!"
} | ConvertTo-Json

$login = Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/auth/login" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body

$TOKEN = $login.access_token
```

Then recreate the Authorization header.

---

## Error: Port already in use

If port `8000` is already being used, stop the existing Uvicorn process or use another port:

```powershell
uvicorn app:app --reload --port 8001
```

Then use:

```text
http://127.0.0.1:8001
```

---

# Final Testing Checklist

Before submission, verify all of the following.

### Server

- [ ] FastAPI starts successfully
- [ ] `/health` returns HTTP 200
- [ ] Swagger opens at `/docs`

### Authentication

- [ ] Signup works
- [ ] Login works
- [ ] JWT access token is returned
- [ ] Invalid credentials are rejected

### Public Route

- [ ] `/public` works without JWT

### Protected Routes

- [ ] `/protected` rejects requests without JWT
- [ ] `/protected` accepts valid JWT
- [ ] Invalid JWT is rejected
- [ ] `/dashboard` requires JWT
- [ ] `/dashboard` works with valid JWT

### Logout

- [ ] `/auth/logout` requires authentication
- [ ] Logout request works with valid JWT

### Swagger

- [ ] Authorize button is available
- [ ] Bearer JWT can be entered
- [ ] Protected endpoints work from Swagger

### Security

- [ ] `.env` exists locally
- [ ] `.env` is NOT tracked by Git
- [ ] `.env.example` exists
- [ ] No real credentials are committed
- [ ] No JWT tokens are committed
- [ ] `.venv/` is ignored

### GitHub

- [ ] README is committed
- [ ] `.gitignore` is committed
- [ ] `.env.example` is committed
- [ ] `requirements.txt` is committed
- [ ] Source code is committed
- [ ] Changes are pushed to `origin/main`

---

# Final API Summary

```text
GET  /health
POST /auth/signup
POST /auth/login
GET  /public
GET  /protected
GET  /dashboard
POST /auth/logout
```

---

# License

This project was created as part of the FlyRank assignment.