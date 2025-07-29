# 🗂️ Taskify – Task Manager Web App

Taskify is a modern, dark-mode task management web app built using **Django** and **Tailwind CSS**.  
Users can create, update, filter, and manage tasks with a clean and intuitive UI.

## 🔥 Features
- User Registration & Login
- Add / Edit / Delete Tasks
- Filter by Status / Priority / Overdue
- Live priority/status update from list view
- Mobile-friendly and fully responsive
- Beautiful dark-mode UI

## 🛠️ Tech Stack
- Django (Backend)
- HTML + Tailwind CSS (Frontend)
- SQLite (for demo)

## 🚀 Getting Started (Local Setup)
```bash
git clone https://github.com/VinayJDevHub/Taskify.git
cd Taskify
python -m venv env
source env/bin/activate   # Windows: env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
