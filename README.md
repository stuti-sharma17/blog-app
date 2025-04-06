# Khayal – Full-Stack Blog Platform 📝✨

**Khayal** is a full-fledged full-stack blog application built with Django, Django REST Framework, and PostgreSQL. It supports AI-based tweet suggestions, full CRUD operations, secure authentication, and a polished UI using Bootstrap.

## 🚀 Features

- 🧠 AI Tweet Idea Generator using GPT-2 (Hugging Face)
- ✅ User Authentication (Register/Login/Logout)
- ✍️ Tweet Creation, Editing, Deletion (CRUD)
- 🔍 Backend Search & Filters
- 🧵 Tweet Titles + Bootstrap Modal Previews
- 📁 Media Uploads (Profile Pictures & Tweets)
- 👤 User Profile Pages with Edit Support
- 🔐 Token-based API Authentication
- 🛠️ Modular Django Template Design (with Sidebar Layout)
- 🎨 Pastel-Themed UI with Animations
- 📦 Optimized PostgreSQL Queries & Soft Deletion (Planned)
- 🔌 REST API Endpoints for Integration & Extensibility

## 🧠 AI Integration

- Utilizes Hugging Face's `gpt2` model to generate creative tweet ideas.
- Modular design using `tweet/utils/ai_generator.py`.
- Available only to logged-in users via a protected route.

## 🛠️ Technologies Used

| Category           | Stack                                             |
|--------------------|--------------------------------------------------|
| Languages          | Python, JavaScript, HTML, CSS, SQL               |
| Frameworks         | Django, DRF, Bootstrap, AJAX                     |
| Tools & Platforms  | PostgreSQL, Git, GitHub, pgAdmin, VS Code        |
| AI/ML Integration  | Hugging Face Transformers, `gpt2`, `transformers`|

## 📥 Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/stuti-sharma17/blog-app.git
   cd blog-app
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
4. Run migrations & start server:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver

