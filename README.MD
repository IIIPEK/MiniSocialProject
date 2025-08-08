# MiniSocialProject
A Django-based social platform for educational purposes, featuring user authentication, posts, likes, comments, follows, and private messaging.

## Installation
1. Clone the repository: `git clone https://github.com/IIIPEK/MiniSocialProject.git`
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in settings (e.g., `SECRET_KEY`, `EMAIL_*`, `TELEGRAM_BOT_TOKEN`)
6. Generate migrations: `python manage.py makemigrations`
7. Apply migrations: `python manage.py migrate`
8. Create superuser: `python manage.py createsuperuser`
9. Run the server: `python manage.py runserver`

## Features
- User authentication (registration, login, password reset, email confirmation)
- Social features (posts, likes, comments, follows)
- Private messaging
- Notifications (in-app, with optional Telegram integration)
- Django admin panel for content management