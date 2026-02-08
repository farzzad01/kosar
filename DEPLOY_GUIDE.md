# راهنمای دیپلوی روی Render.com

## مراحل دیپلوی

### 1. آماده‌سازی کد
```bash
# اطمینان از وجود تمام فایل‌ها
git init
git add .
git commit -m "Initial commit"
```

### 2. ایجاد ریپازیتوری GitHub
1. وارد GitHub شوید
2. New Repository بسازید
3. کد را push کنید:
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### 3. دیپلوی روی Render.com

#### مرحله 1: ایجاد Web Service
1. وارد [Render.com](https://render.com) شوید
2. New → Web Service
3. Connect GitHub repository
4. تنظیمات:
   - **Name**: `nobatdehi` (یا هر نام دلخواه)
   - **Environment**: `Python 3`
   - **Build Command**: `sh build.sh`
   - **Start Command**: `gunicorn nobatdehi.wsgi:application`

#### مرحله 2: تنظیم Environment Variables
در بخش Environment Variables این متغیرها را اضافه کنید:

```
SECRET_KEY = یک کلید تصادفی قوی (می‌توانید از https://djecrety.ir استفاده کنید)
DEBUG = False
ALLOWED_HOSTS = your-app-name.onrender.com
PYTHON_VERSION = 3.11.7
```

#### مرحله 3: ایجاد PostgreSQL Database (اختیاری)
1. New → PostgreSQL
2. نام دیتابیس را وارد کنید
3. بعد از ایجاد، `DATABASE_URL` را کپی کنید
4. در Web Service، Environment Variable جدید اضافه کنید:
```
DATABASE_URL = [URL کپی شده]
```

#### مرحله 4: Deploy
1. روی "Create Web Service" کلیک کنید
2. منتظر بمانید تا build تمام شود (5-10 دقیقه)
3. بعد از موفقیت، لینک سایت شما نمایش داده می‌شود

### 4. ایجاد Superuser در Production

بعد از دیپلوی موفق:
1. وارد Shell شوید از طریق Render Dashboard
2. دستور زیر را اجرا کنید:
```bash
python manage.py createsuperuser
```

### 5. تنظیم Cron Job برای ریست روزانه

در Render Dashboard:
1. New → Cron Job
2. تنظیمات:
   - **Name**: `daily-reset`
   - **Command**: `python manage.py daily_reset`
   - **Schedule**: `0 0 * * *` (هر روز ساعت 12 شب)

## لینک‌های مهم

- **سایت شما**: `https://your-app-name.onrender.com`
- **پنل ادمین**: `https://your-app-name.onrender.com/admin/`

## نکات مهم

⚠️ **امنیت:**
- هرگز SECRET_KEY را در GitHub قرار ندهید
- DEBUG را در production روی False قرار دهید
- ALLOWED_HOSTS را محدود کنید

⚠️ **دیتابیس:**
- SQLite برای production توصیه نمی‌شود
- حتماً PostgreSQL استفاده کنید

⚠️ **Static Files:**
- Whitenoise به صورت خودکار فایل‌های استاتیک را serve می‌کند
- نیازی به تنظیمات اضافی نیست

## عیب‌یابی

### خطای 500
- لاگ‌ها را در Render Dashboard بررسی کنید
- مطمئن شوید migrations اجرا شده‌اند
- Environment Variables را چک کنید

### Static Files لود نمی‌شوند
```bash
python manage.py collectstatic --no-input
```

### دیتابیس خالی است
```bash
python manage.py migrate
python manage.py createsuperuser
```

## پشتیبانی

برای مشکلات، لاگ‌های Render را بررسی کنید:
Dashboard → Your Service → Logs
