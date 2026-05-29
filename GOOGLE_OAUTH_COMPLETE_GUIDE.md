# راهنمای کامل تنظیمات Google OAuth برای سیستم ثبت‌نام

## 📋 فهرست مطالب
1. [تنظیمات Google Cloud Console](#1-تنظیمات-google-cloud-console)
2. [تنظیمات Vercel](#2-تنظیمات-vercel)
3. [تنظیمات محلی (Local Development)](#3-تنظیمات-محلی)
4. [تست و عیب‌یابی](#4-تست-و-عیب‌یابی)

---

## 1. تنظیمات Google Cloud Console

### مرحله 1: ایجاد پروژه جدید
1. به [Google Cloud Console](https://console.cloud.google.com/) بروید
2. روی **Select a project** کلیک کنید
3. **New Project** را انتخاب کنید
4. نام پروژه را وارد کنید (مثلاً: `Student Registration System`)
5. روی **Create** کلیک کنید

### مرحله 2: فعال‌سازی Google+ API
1. در منوی سمت چپ، به **APIs & Services** > **Library** بروید
2. جستجو کنید: `Google+ API`
3. روی **Google+ API** کلیک کنید
4. روی **Enable** کلیک کنید

### مرحله 3: ایجاد OAuth 2.0 Credentials
1. به **APIs & Services** > **Credentials** بروید
2. روی **+ CREATE CREDENTIALS** کلیک کنید
3. **OAuth client ID** را انتخاب کنید
4. اگر اولین بار است، باید **OAuth consent screen** را پیکربندی کنید:

#### پیکربندی OAuth Consent Screen:
- **User Type**: External را انتخاب کنید
- **App name**: نام برنامه خود را وارد کنید
- **User support email**: ایمیل خود را وارد کنید
- **Developer contact information**: ایمیل خود را وارد کنید
- روی **Save and Continue** کلیک کنید
- در بخش **Scopes**، این موارد را اضافه کنید:
  - `email`
  - `profile`
  - `openid`
- روی **Save and Continue** کلیک کنید
- در بخش **Test users**، ایمیل‌های تست خود را اضافه کنید (اختیاری)
- روی **Save and Continue** کلیک کنید

### مرحله 4: ایجاد OAuth Client ID
1. دوباره به **Credentials** بروید
2. **+ CREATE CREDENTIALS** > **OAuth client ID**
3. **Application type**: Web application
4. **Name**: نام دلخواه (مثلاً: `Student Registration OAuth`)
5. **Authorized JavaScript origins**:
   ```
   https://your-domain.vercel.app
   http://localhost:8000
   ```
6. **Authorized redirect URIs**:
   ```
   https://your-domain.vercel.app/accounts/google/login/callback/
   https://your-domain.vercel.app/auth/google/callback/
   http://localhost:8000/accounts/google/login/callback/
   http://localhost:8000/auth/google/callback/
   ```
7. روی **Create** کلیک کنید
8. **Client ID** و **Client Secret** را کپی کنید و در جای امنی ذخیره کنید

---

## 2. تنظیمات Vercel

### مرحله 1: اضافه کردن Environment Variables
1. به [Vercel Dashboard](https://vercel.com/dashboard) بروید
2. پروژه خود را انتخاب کنید
3. به **Settings** > **Environment Variables** بروید
4. این متغیرها را اضافه کنید:

```bash
# Google OAuth Settings
GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret-here

# Django Settings (اگر قبلاً اضافه نکرده‌اید)
SECRET_KEY=your-django-secret-key-here
DEBUG=False
ALLOWED_HOSTS=.vercel.app,.now.sh

# Database (اگر از PostgreSQL استفاده می‌کنید)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# reCAPTCHA (اگر دارید)
RECAPTCHA_PUBLIC_KEY=your-recaptcha-public-key
RECAPTCHA_PRIVATE_KEY=your-recaptcha-private-key
```

### مرحله 2: Deploy مجدد
1. بعد از اضافه کردن Environment Variables، پروژه را دوباره deploy کنید:
   ```bash
   git add .
   git commit -m "Add Google OAuth support"
   git push
   ```
2. یا از Vercel Dashboard روی **Redeploy** کلیک کنید

### مرحله 3: به‌روزرسانی Redirect URIs در Google Console
1. دوباره به Google Cloud Console بروید
2. به **Credentials** بروید
3. OAuth Client ID خود را ویرایش کنید
4. **Authorized redirect URIs** را با URL واقعی Vercel خود به‌روز کنید:
   ```
   https://your-actual-domain.vercel.app/accounts/google/login/callback/
   https://your-actual-domain.vercel.app/auth/google/callback/
   ```

---

## 3. تنظیمات محلی (Local Development)

### مرحله 1: ایجاد فایل .env
در ریشه پروژه، فایل `.env` ایجاد کنید:

```bash
# Google OAuth
GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret-here

# Django
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# reCAPTCHA
RECAPTCHA_PUBLIC_KEY=6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI
RECAPTCHA_PRIVATE_KEY=6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe
```

### مرحله 2: نصب Dependencies
```bash
pip install -r requirements.txt
```

### مرحله 3: اجرای Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### مرحله 4: ایجاد Superuser
```bash
python manage.py createsuperuser
```

### مرحله 5: اجرای سرور محلی
```bash
python manage.py runserver
```

### مرحله 6: تنظیمات Django Admin
1. به `http://localhost:8000/secret-admin-panel-xyz/` بروید
2. با superuser لاگین کنید
3. به **Sites** بروید و domain را به `localhost:8000` تغییر دهید
4. به **Social applications** بروید
5. **Add social application** را کلیک کنید:
   - **Provider**: Google
   - **Name**: Google OAuth
   - **Client id**: کلاینت آیدی خود را وارد کنید
   - **Secret key**: سکرت کی خود را وارد کنید
   - **Sites**: localhost:8000 را انتخاب کنید
   - **Save** کنید

---

## 4. تست و عیب‌یابی

### تست لاگین با Google
1. به صفحه لاگین بروید: `/login/`
2. روی دکمه **تسجيل الدخول باستخدام Google** کلیک کنید
3. اکانت Google خود را انتخاب کنید
4. اجازه دسترسی به برنامه را بدهید
5. باید به پنل ادمین هدایت شوید

### مشکلات رایج و راه‌حل‌ها

#### خطا: "redirect_uri_mismatch"
**راه‌حل:**
- مطمئن شوید که Redirect URI در Google Console دقیقاً با URL برنامه شما مطابقت دارد
- حتماً `/` در انتهای URL را فراموش نکنید
- بعد از تغییر، چند دقیقه صبر کنید تا تغییرات اعمال شود

#### خطا: "invalid_client"
**راه‌حل:**
- Client ID و Client Secret را دوباره چک کنید
- مطمئن شوید که در Environment Variables درست وارد شده‌اند
- پروژه را دوباره deploy کنید

#### خطا: "SocialApp matching query does not exist"
**راه‌حل:**
- به Django Admin بروید
- Social Application را ایجاد کنید (مرحله 6 بالا)
- مطمئن شوید که Site درست انتخاب شده است

#### لاگین کار نمی‌کند
**راه‌حل:**
1. لاگ‌های Vercel را چک کنید:
   ```bash
   vercel logs
   ```
2. مطمئن شوید که تمام Environment Variables درست تنظیم شده‌اند
3. مطمئن شوید که migrations اجرا شده‌اند
4. Database connection را چک کنید

---

## 🔐 نکات امنیتی

1. **هرگز Client Secret را در کد قرار ندهید** - فقط در Environment Variables
2. **HTTPS را در production فعال کنید** - Google OAuth به HTTPS نیاز دارد
3. **DEBUG را در production خاموش کنید** - `DEBUG=False`
4. **SECRET_KEY را تصادفی و پیچیده انتخاب کنید**
5. **فایل .env را به .gitignore اضافه کنید**

---

## 📱 لینک‌های مفید

- [Google Cloud Console](https://console.cloud.google.com/)
- [Django Allauth Documentation](https://django-allauth.readthedocs.io/)
- [Vercel Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)
- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)

---

## ✅ چک‌لیست نهایی

- [ ] پروژه در Google Cloud Console ایجاد شد
- [ ] Google+ API فعال شد
- [ ] OAuth Client ID ایجاد شد
- [ ] Redirect URIs درست تنظیم شدند
- [ ] Environment Variables در Vercel اضافه شدند
- [ ] Dependencies نصب شدند (`django-allauth`, `google-auth`)
- [ ] Migrations اجرا شدند
- [ ] Social Application در Django Admin ایجاد شد
- [ ] تست لاگین با Google انجام شد
- [ ] همه چیز کار می‌کند! 🎉

---

## 🆘 نیاز به کمک؟

اگر مشکلی داشتید:
1. لاگ‌های Vercel را چک کنید
2. Console Browser را چک کنید (F12)
3. مطمئن شوید که تمام مراحل را دنبال کرده‌اید
4. Google OAuth errors را جستجو کنید

موفق باشید! 🚀
