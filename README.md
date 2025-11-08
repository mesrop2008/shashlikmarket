# 🍢 Shashlik Market — Django Food Ordering Website

## 🧾 About the Project

**Shashlik Market** is a full-featured **food ordering website** built with **Django**.  
It allows users to browse a restaurant’s menu, add dishes to a shopping cart, and place online food orders quickly and conveniently.  
The project includes an **admin panel** for managing menu items, orders, and media files.  

This application demonstrates how to build a **complete online food delivery system** using Django, PostgreSQL, and Cloudinary.  
It was developed as a **portfolio project** to showcase full-stack web development skills — from backend logic and database setup to file storage and environment configuration.

---

## 🚀 Features

- 🍔 Full food ordering workflow (menu, cart, orders)
- 🧾 Admin panel for managing items and orders
- 🗄️ PostgreSQL database
- ☁️ Cloudinary integration for image/media storage
- 🌍 Russian localization and timezone support
- 🔐 Secure `.env` configuration for sensitive data

---

## 🛠️ Installation Guide

### 1. Clone the repository
```bash
git clone https://github.com/<mesrop2008>/<shashlikmarket>.git
cd <shashlikmarket>
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate       # macOS/Linux
venv\Scripts\activate        # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` file
Create a `.env` file in the root directory (next to `manage.py`) and fill it based on `.env.example`:

```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=127.0.0.1
DB_PORT=5432

CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

---

### 5. Apply database migrations
```bash
python manage.py migrate
```

### 6. Create a superuser (for admin access)
```bash
python manage.py createsuperuser
```

### 7. Run the development server
```bash
python manage.py runserver
```

Now open your browser at:  
👉 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 📦 Environment Variables

| Variable | Description |
|-----------|--------------|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Enables debug mode (`True` for dev, `False` for prod) |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | PostgreSQL configuration |
| `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET` | Cloudinary credentials |

---

## 🧩 Tech Stack

- **Python 3.x**
- **Django 5.x**
- **PostgreSQL**
- **Cloudinary**
- **python-dotenv**

---

## 📂 Project Structure

```bash
MYSITE/
├── mysite/               # Project settings
├── shashlikmarket/       # Main Django app
├── manage.py
├── requirements.txt
├── .env                  # Environment variables (ignored by git)
├── .env.example          # Example configuration file
└── .gitignore
```

---

---

## 💡 Possible Future Improvements

- 💳 Online payment integration 
- 🕒 Real-time order tracking and delivery estimation  

---

## 🧠 Author

Developed by **Mesrop**  
This project is open-source — feel free to use, modify, and contribute!

---


