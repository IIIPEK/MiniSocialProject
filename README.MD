# MiniSocial Project

*[Русская версия](#русская-версия)*

## English Version

### 📱 About

MiniSocial is a lightweight social networking platform built with Django. It provides essential social media features including user profiles, posts, comments, likes, following system, and real-time notifications.

### ✨ Features

- **User Management**
  - Custom user registration and authentication
  - Email confirmation system
  - Profile management with avatars, bio, and social links
  - Password reset functionality

- **Social Features**
  - Create, edit, and delete posts with text and images
  - Like/unlike posts
  - Comment system
  - Follow/unfollow users
  - User search and discovery

- **Feed System**
  - Personalized post feed
  - Filter options: All posts, Following only, Non-following, Followers
  - Search posts by content, title, or author
  - Sort by date or popularity (likes/comments)

- **Notifications**
  - Real-time notifications for likes, comments, and follows
  - Notification management (mark as read)

- **Admin Features**
  - Django admin interface
  - User management
  - Content moderation

### 🛠 Technology Stack

- **Backend**: Django 5.2.3
- **Database**: SQLite (development)
- **Frontend**: Bootstrap 5.3.0, Vanilla JavaScript
- **Authentication**: Django built-in auth system
- **File Storage**: Local file system
- **Email**: SMTP backend

### 📋 Requirements

- Python 3.8+
- Django 5.2.3
- python-dotenv
- Pillow (for image handling)

### 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd MiniSocial_Project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django python-dotenv pillow
   ```

4. **Environment setup**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` file with your configuration:
   ```
   EMAIL_HOST=smtp.your_server.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your_mail@your_domain.com
   EMAIL_HOST_PASSWORD=Your_Strong_Mail_Password
   DEFAULT_FROM_EMAIL=your_mail@your_domain.com
   MAIN_TITLE=MiniSocial
   SECRET_KEY=your-secret-key-here
   DJANGO_DEBUG=True
   ```

5. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

### 📁 Project Structure

```
MiniSocial_Project/
├── accounts/           # User management app
├── core/              # Core functionality and home page
├── social/            # Posts, comments, likes functionality
├── notifications/     # Notification system
├── utils/             # Utilities and template tags
├── templates/         # HTML templates
├── media/            # User uploaded files
├── manage.py
└── requirements files
```

### 🎯 Usage

1. **Registration**: Create account with email confirmation
2. **Profile Setup**: Add avatar, bio, and social links
3. **Create Content**: Share posts with text and images
4. **Social Interaction**: Like, comment, and follow other users
5. **Discover**: Use search and filters to find interesting content
6. **Stay Updated**: Receive notifications for interactions

### ⚙️ Configuration

Key settings in `settings.py`:

- `COMMENT_DELETE_DAYS = 7`: Days to allow comment deletion
- `POST_DELETE_DAYS = 30`: Days to allow post deletion  
- `POST_EDIT_DAYS = 7`: Days to allow post editing
- `AUTH_USER_MODEL = 'accounts.CustomUser'`: Custom user model

### 🔒 Security Features

- Email confirmation required for full account activation
- CSRF protection on all forms
- User permissions for content modification
- Time-limited editing/deletion of posts and comments

### 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## Русская версия

### 📱 О проекте

MiniSocial — это легкая платформа социальной сети, построенная на Django. Она предоставляет основные функции социальных сетей, включая профили пользователей, посты, комментарии, лайки, систему подписок и уведомления в реальном времени.

### ✨ Функции

- **Управление пользователями**
  - Регистрация и аутентификация пользователей
  - Система подтверждения email
  - Управление профилем с аватарами, биографией и социальными ссылками
  - Функция сброса пароля

- **Социальные функции**
  - Создание, редактирование и удаление постов с текстом и изображениями
  - Лайки/дизлайки постов
  - Система комментариев
  - Подписка/отписка от пользователей
  - Поиск и обнаружение пользователей

- **Система ленты**
  - Персонализированная лента постов
  - Опции фильтрации: Все посты, Только подписки, Кого не читаю, Подписчики
  - Поиск постов по содержанию, заголовку или автору
  - Сортировка по дате или популярности (лайки/комментарии)

- **Уведомления**
  - Уведомления в реальном времени для лайков, комментариев и подписок
  - Управление уведомлениями (пометка как прочитанное)

- **Административные функции**
  - Интерфейс Django admin
  - Управление пользователями
  - Модерация контента

### 🛠 Технологический стек

- **Backend**: Django 5.2.3
- **База данных**: SQLite (разработка)
- **Frontend**: Bootstrap 5.3.0, Vanilla JavaScript
- **Аутентификация**: Встроенная система Django
- **Хранение файлов**: Локальная файловая система
- **Email**: SMTP backend

### 📋 Требования

- Python 3.8+
- Django 5.2.3
- python-dotenv
- Pillow (для обработки изображений)

### 🚀 Установка

1. **Клонирование репозитория**
   ```bash
   git clone <url-репозитория>
   cd MiniSocial_Project
   ```

2. **Создание виртуального окружения**
   ```bash
   python -m venv venv
   source venv/bin/activate  # На Windows: venv\Scripts\activate
   ```

3. **Установка зависимостей**
   ```bash
   pip install django python-dotenv pillow
   ```

4. **Настройка окружения**
   ```bash
   cp .env.example .env
   ```
   Отредактируйте файл `.env` с вашей конфигурацией:
   ```
   EMAIL_HOST=smtp.your_server.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your_mail@your_domain.com
   EMAIL_HOST_PASSWORD=Your_Strong_Mail_Password
   DEFAULT_FROM_EMAIL=your_mail@your_domain.com
   MAIN_TITLE=MiniSocial
   SECRET_KEY=your-secret-key-here
   DJANGO_DEBUG=True
   ```

5. **Настройка базы данных**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Создание суперпользователя**
   ```bash
   python manage.py createsuperuser
   ```

7. **Запуск сервера разработки**
   ```bash
   python manage.py runserver
   ```

### 📁 Структура проекта

```
MiniSocial_Project/
├── accounts/           # Приложение управления пользователями
├── core/              # Основной функционал и главная страница
├── social/            # Функционал постов, комментариев, лайков
├── notifications/     # Система уведомлений
├── utils/             # Утилиты и теги шаблонов
├── templates/         # HTML шаблоны
├── media/            # Загруженные пользователями файлы
├── manage.py
└── файлы требований
```

### 🎯 Использование

1. **Регистрация**: Создайте аккаунт с подтверждением email
2. **Настройка профиля**: Добавьте аватар, биографию и социальные ссылки
3. **Создание контента**: Делитесь постами с текстом и изображениями
4. **Социальное взаимодействие**: Ставьте лайки, комментируйте и подписывайтесь на других пользователей
5. **Исследование**: Используйте поиск и фильтры для поиска интересного контента
6. **Оставайтесь в курсе**: Получайте уведомления о взаимодействиях

### ⚙️ Конфигурация

Ключевые настройки в `settings.py`:

- `COMMENT_DELETE_DAYS = 7`: Дни для разрешения удаления комментариев
- `POST_DELETE_DAYS = 30`: Дни для разрешения удаления постов
- `POST_EDIT_DAYS = 7`: Дни для разрешения редактирования постов
- `AUTH_USER_MODEL = 'accounts.CustomUser'`: Пользовательская модель пользователя

### 🔒 Функции безопасности

- Требуется подтверждение email для полной активации аккаунта
- CSRF защита на всех формах
- Разрешения пользователей для модификации контента
- Ограниченное по времени редактирование/удаление постов и комментариев

### 🤝 Участие в разработке

1. Форкните репозиторий
2. Создайте ветку функции (`git checkout -b feature/AmazingFeature`)
3. Зафиксируйте изменения (`git commit -m 'Add AmazingFeature'`)
4. Отправьте в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

### 📝 Лицензия

Этот проект является открытым исходным кодом и доступен под [лицензией MIT](LICENSE).