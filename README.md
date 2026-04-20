# YUSAN TECH — Student Management System

Official Student Admission Portal built with Django.

---

## 🚀 Run Locally (Termux / PC)

```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open: `http://127.0.0.1:8000`

---

## 🌐 Deploy on Railway

1. Push to GitHub (steps below)
2. Go to railway.app → New Project → Deploy from GitHub
3. Add environment variable: `SECRET_KEY` = any random string
4. Done! Railway auto-deploys ✅

---

## 📤 Upload to GitHub

```bash
git init
git add .
git commit -m "YUSAN TECH first upload"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/yusan-tech.git
git push -u origin main
```

---

## 📁 Pages

| Page | URL |
|------|-----|
| Home | `/` |
| Register | `/register/` |
| Login | `/login/` |
| Dashboard | `/dashboard/` |
| Admin | `/admin/` |

---

**Created by YUSAN TECH GROUP | Powered by ASAF TECH CORP**
# yusan
