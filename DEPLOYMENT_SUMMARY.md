# خلاصه تغییرات و راهنمای Deploy

## ✅ تغییرات انجام شده

### 1. لوگو در صفحه Registration
- لوگو از مسیر `assets/logoi.png` در صفحه `registration.html` قرار گرفت
- Fallback برای لوگو اضافه شد

### 2. سیستم لاگین با Google OAuth
- صفحه لاگین جدید ایجاد شد: `templates/login.html`
- دکمه لاگین با Google اضافه شد
- فرم لاگین سنتی (ایمیل/پسورد) هم موجود است

### 3. تنظیمات Django
- `django-allauth` برای Google OAuth اضافه شد
- Authentication backends پیکربندی شد
- URLهای جدید برای لاگین اضافه شدند:
  - `/login/` - صفحه لاگین
  - `/auth/google/` - شروع OAuth با Google
  - `/auth/google/callback/` - Callback از Google
  - `/accounts/google/login/callback/` - Callback allauth

### 4. Dependencies جدید
```
django-allauth==0.57.0
google-auth==2.23.4
google-auth-oauthlib==1.1.0
google-auth-httplib2==0.1.1
```

---

## 🚀 مراحل Deploy

### مرحله 1: Push کردن کد
```bash
git add .
git commit -m "Add Google OAuth and update logo"
git push origin main
```

### مرحله 2: تنظیمات Vercel Environment Variables
به Vercel Dashboard بروید و این متغیرها را اضافه کنید:

```bash
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
SECRET_KEY=your-django-secret-key
DEBUG=False
```

### مرحله 3: تنظیمات Google Cloud Console
1. به [Google Cloud Console](https://console.cloud.google.com/) بروید
2. پروژه جدید ایجاد کنید یا پروژه موجود را انتخاب کنید
3. Google+ API را فعال کنید
4. OAuth 2.0 Client ID ایجاد کنید
5. Authorized redirect URIs را اضافه کنید:
   ```
   https://your-domain.vercel.app/accounts/google/login/callback/
   https://your-domain.vercel.app/auth/google/callback/
   ```

### مرحله 4: Deploy در Vercel
```bash
vercel --prod
```

یا از Vercel Dashboard روی **Redeploy** کلیک کنید.

### مرحله 5: تنظیمات Django Admin (بعد از Deploy)
1. به پنل ادمین بروید: `https://your-domain.vercel.app/secret-admin-panel-xyz/`
2. به **Sites** بروید و domain را به domain واقعی خود تغییر دهید
3. به **Social applications** بروید
4. **Add social application** کنید:
   - Provider: Google
   - Name: Google OAuth
   - Client id: کلاینت آیدی از Google Console
   - Secret key: سکرت کی از Google Console
   - Sites: سایت خود را انتخاب کنید

---

## 📝 راهنمای کامل

برای راهنمای کامل و جزئیات بیشتر، فایل `GOOGLE_OAUTH_COMPLETE_GUIDE.md` را مطالعه کنید.

این راهنما شامل:
- تنظیمات دقیق Google Cloud Console
- تنظیمات Vercel
- تنظیمات محلی برای Development
- عیب‌یابی مشکلات رایج
- نکات امنیتی

---

## 🔗 لینک‌های مهم

- صفحه لاگین: `/login/`
- صفحه ثبت‌نام: `/` (registration)
- پنل ادمین: `/secret-admin-panel-xyz/`

---

## ⚠️ نکات مهم

1. **حتماً Environment Variables را در Vercel تنظیم کنید**
2. **Redirect URIs در Google Console باید دقیقاً با domain شما مطابقت داشته باشد**
3. **بعد از Deploy، حتماً Social Application را در Django Admin ایجاد کنید**
4. **اگر مشکلی داشتید، لاگ‌های Vercel را چک کنید: `vercel logs`**

موفق باشید! 🎉
