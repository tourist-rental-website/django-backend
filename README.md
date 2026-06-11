# Tourist Rental Platform Backend

A modular Django backend API designed for the Tourist Rental Platform. This project provides RESTful APIs for user registration, authentications (via JWT tokens), profile management, and property listings.

---

## 🛠️ Technology Stack

* **Framework:** Django 6.0.6 & Django REST Framework (DRF)
* **Authentication:** JWT (JSON Web Tokens) via `djangorestframework-simplejwt`
* **Database:** PostgreSQL
* **Environment Variables:** `python-decouple`

---

## 🐘 PostgreSQL Database Setup

The backend utilizes PostgreSQL as its primary database. Follow the steps below to install PostgreSQL and prepare the database.

### 1. Install PostgreSQL

#### On Ubuntu / Debian:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

#### On macOS (using Homebrew):
```bash
brew install postgresql@14
brew services start postgresql@14
```

#### On Windows:
1. Download the installer from the [PostgreSQL Official Website](https://www.postgresql.org/download/windows/).
2. Run the installer and configure the `postgres` user password (we recommend using `postgres` for local development setup).

---

### 2. Configure Database & User

Once installed, log into the PostgreSQL interactive terminal to create the database and user matching your `.env` configuration.

#### Open PostgreSQL Shell
```bash
sudo -u postgres psql
```

#### Run SQL Commands in psql:
```sql
-- Create the database
CREATE DATABASE tourist_rental_db;

-- Create the database user (replace 'postgres' with your desired password)
CREATE USER travel_user WITH PASSWORD 'postgres';

-- Grant privileges to the user
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE tourist_rental_db TO postgres;

-- Exit the shell
\q
```

---

### 3. Configure the Environment File (`.env`)

Create or update a `.env` file in the backend root directory `/backend/.env` with your database credentials:

```ini
# Django settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL Database Configuration
DB_NAME=tourist_rental_db
DB_USER=travel_user
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:4200
```

---

## 🚀 Getting Started

Follow these instructions to set up the Python environment and run the development server.

### 1. Set Up Virtual Environment

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows (cmd):
venv\Scripts\activate.bat
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run Database Migrations

Apply the database schema changes to PostgreSQL:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (Admin Access)

Create an admin account to access the Django Admin Portal:

```bash
python manage.py createsuperuser
```

### 5. Start the Development Server

```bash
python manage.py runserver
```
The server will start running at `http://127.0.0.1:8000/`. You can access the Admin panel at `http://127.0.0.1:8000/admin/`.

---

## 🔑 Authentication & API Endpoints

The accounts app provides JSON REST endpoints for authenticating users. All request payloads must have the header `Content-Type: application/json`.

### Endpoints Overview

| Endpoint | Method | Authentication Required | Description |
| :--- | :--- | :--- | :--- |
| `/accounts/api/register/` | `POST` | None | Register a new user and retrieve tokens immediately. |
| `/accounts/api/login/` | `POST` | None | Log in with credentials and receive access and refresh tokens. |
| `/accounts/api/token/refresh/` | `POST` | None | Refresh an expired access token using a refresh token. |
| `/accounts/api/profile/` | `GET` / `PUT` / `PATCH` | JWT (Bearer Token) | Retrieve or update current user's profile details. |

---

### Example cURL Commands

#### 1. User Registration (`POST`)
* **Endpoint:** `/accounts/api/register/`
* **Request Body:**
```json
{
  "email": "user@example.com",
  "password": "strong_password123",
  "first_name": "John",
  "last_name": "Doe"
}
```
* **cURL Command:**
```bash
curl -X POST http://127.0.0.1:8000/accounts/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "strong_password123", "first_name": "John", "last_name": "Doe"}'
```

#### 2. User Login / Obtain Token (`POST`)
* **Endpoint:** `/accounts/api/login/`
* **Request Body:**
```json
{
  "email": "user@example.com",
  "password": "strong_password123"
}
```
* **cURL Command:**
```bash
curl -X POST http://127.0.0.1:8000/accounts/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "strong_password123"}'
```

#### 3. Refresh Access Token (`POST`)
* **Endpoint:** `/accounts/api/token/refresh/`
* **Request Body:**
```json
{
  "refresh": "<your_refresh_token>"
}
```
* **cURL Command:**
```bash
curl -X POST http://127.0.0.1:8000/accounts/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "your_refresh_token_here"}'
```

#### 4. Access User Profile (`GET`)
* **Endpoint:** `/accounts/api/profile/`
* **Authorization Header:** `Bearer <your_access_token>`
* **cURL Command:**
```bash
curl -X GET http://127.0.0.1:8000/accounts/api/profile/ \
  -H "Authorization: Bearer your_access_token_here" \
  -H "Content-Type: application/json"
```
### PostgreSQL Setup

After creating the database and application user, grant the required permissions before running Django migrations.

Example:

```SQL
CREATE DATABASE tourist_rental_db;

CREATE USER travel_user WITH PASSWORD 'your_password';

GRANT ALL ON SCHEMA public TO travel_user;

GRANT ALL PRIVILEGES ON DATABASE tourist_rental_db TO travel_user;

ALTER DATABASE tourist_rental_db OWNER TO travel_user;
```

Why is this necessary?

Django migrations create database tables. If the application user does not have permissions on the `public` schema, migrations will fail with:

```
permission denied for schema public
```

Run these commands before executing:

```bash
python manage.py migrate
```
- Setup Order
1. Install PostgreSQL
2. Create database
3. Create application user
4. Grant schema/database permissions
5. Configure .env
6. Run migrations