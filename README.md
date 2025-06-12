# 📸 Photo Gallery API

This is a RESTful API developed using **Python (Flask)** that allows users to **register, authenticate, view, like, and manage photos**. Authenticated users can see photos uploaded by others, view a random daily photo, and like photos. Admin users have access to additional management capabilities.

---

## 🚀 Features

- User registration and login with JWT authentication  
- Role-based access control (user / admin)  
- Upload photos with metadata (URL, dimensions, color, etc.)  
- View all photos, individual photos, or photos by photographer  
- Like/unlike photos  
- Retrieve a random daily photo (no authentication required)  
- CORS-enabled to allow frontend integration  
- SQLite or PostgreSQL-ready using `psycopg2`

---

## 🛠️ Tech Stack

- Python 3.x  
- Flask  
- PostgreSQL  
- bcrypt  
- JWT (JSON Web Tokens)  
- psycopg2 (PostgreSQL driver)  
- Flask-CORS  

---
## ⚙️ Installation

### 1. Clone repository

```bash
git clone https://github.com/jvscardoso/photo-app-api.git
cd photo-app-api.git
```

### 2. Create a virual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Configure environment variables
Make a copy of the `.env.example` file and rename it to `.env`.

### 4. Initialize Docker

```bash
docker-compose up --build
```
> This will install the dependecies in the requirements.txt file and create the PostgreSQL container and run the init_db.sql script. The database won't be populated yet.

### 5. Run migrations
```bash
docker compose exec web python database/migrations/run_migrations.py
```

> This run all the migrations, read the csv file and  will seed the database with some data.

---

## 🔑 Credentials

| E-mail     | Password                                                    |
|----------|---------------------------------------------------------------|
| `admin@clever.io`  | admin123                              |
| `nick@clever.io`| nick123           |
| `lukas@clever.io`   | user123                            |

**Developed by [João Vitor Cardoso]**
