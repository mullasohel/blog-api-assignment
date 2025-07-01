# Blog API Assignment – Sohel Mulla

This is a backend assignment that implements a simple blog API using Django and DRF. It supports real-time notifications using WebSockets and includes Swagger docs.

---

## 🔧 Tech Stack

- Python, Django, Django REST Framework
- PostgreSQL (via Docker)
- Token-based Authentication
- WebSocket (Django Channels)
- Swagger/OpenAPI (drf-yasg)
- Docker + Docker Compose

---

## 🚀 Features

✅ CRUD APIs for Posts and Authors  
✅ Filter Posts by Author or Created Date  
✅ Token Authentication  
✅ Real-time notifications on new post (/ws/posts/)  
✅ Swagger docs at `/swagger/`  
✅ Dockerized setup  
✅ README + Theoretical AWS deployment guide  

---

# Visit Visit: http://localhost:8000/swagger/ to test api documentaion

# 1. Clone repo and enter
git clone <repo_url>
cd blog_project

# 2. Create env and install dependencies
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Run migrations and create superuser
python manage.py migrate
python manage.py createsuperuser

# 4. Run development server
python manage.py runserver

# 5. For WebSocket support, run with Daphne or Uvicorn:
daphne blog_project.asgi:application
# or
uvicorn blog_project.asgi:application --host 0.0.0.0 --port 8000

# 🔐 Authentication
This project uses Token Authentication via Django REST Framework.

Sample Token for testing:

# Token: 1ec32c5389d246dd615494f6959478ab30db7dda
# 🛰 WebSocket Test
Connect to: ws://localhost:8000/ws/posts/

When a post is created, you'll receive a real-time message

# ☁️ AWS Deployment (Theory)
You can deploy using AWS Elastic Beanstalk or EC2 with Docker

Add Nginx + Gunicorn if required in production