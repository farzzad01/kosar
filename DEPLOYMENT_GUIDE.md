# راهنمای دیپلوی در Vercel

## مرحله 1: آماده‌سازی فایل Credentials

1. فایل `decent-destiny-466517-k1-18a0c65a31ea.json` را در ریشه پروژه قرار دهید
2. این فایل را در `.gitignore` قرار دهید (قبلاً اضافه شده)

## مرحله 2: تنظیمات Google Sheets

1. به [Google Sheets](https://sheets.google.com) بروید
2. یک Sheet جدید با نام `Student_Registrations` بسازید
3. Sheet را با ایمیل `vercel-sheets-connector@decent-destiny-466517-k1.iam.gserviceaccount.com` به اشتراک بگذارید
4. دسترسی "Editor" بدهید

## مرحله 3: نصب Vercel CLI

```bash
npm install -g vercel
```

## مرحله 4: لاگین به Vercel

```bash
vercel login
```

## مرحله 5: دیپلوی پروژه

```bash
# اولین بار
vercel

# یا برای production
vercel --prod
```

## مرحله 6: تنظیم Environment Variables در Vercel

در داشبورد Vercel:

1. به Settings > Environment Variables بروید
2. این متغیرها را اضافه کنید:

```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=.vercel.app
```

## مرحله 7: آپلود فایل Credentials

در Vercel Dashboard:
1. به Settings > General بروید
2. فایل JSON را در root directory پروژه قرار دهید

## تست سیستم

بعد از دیپلوی:
1. به URL پروژه بروید
2. فرم را پر کنید
3. Google Sheet را چک کنید

## نکات مهم

✅ **امنیت**: فایل credentials را commit نکنید
✅ **Sheet**: حتماً با service account به اشتراک بگذارید
✅ **دسترسی**: Editor permission لازم است

## دستورات مفید

```bash
# دیپلوی جدید
vercel --prod

# مشاهده لاگ‌ها
vercel logs

# حذف دیپلوی
vercel remove
```

## مشکلات رایج

### خطای Authentication
- چک کنید Sheet با service account به اشتراک گذاشته شده
- فایل JSON را بررسی کنید

### خطای Module Not Found
- `requirements.txt` را چک کنید
- دوباره دیپلوی کنید

### خطای 500
- لاگ‌ها را با `vercel logs` بررسی کنید
