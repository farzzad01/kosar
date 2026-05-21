# راهنمای راه‌اندازی Google Sheets و Drive

## مرحله 1: ایجاد پروژه در Google Cloud Console

1. به [Google Cloud Console](https://console.cloud.google.com/) بروید
2. یک پروژه جدید بسازید (مثلاً "Student Registration System")
3. پروژه را انتخاب کنید

## مرحله 2: فعال‌سازی API ها

1. به بخش "APIs & Services" > "Library" بروید
2. این APIها را جستجو و فعال کنید:
   - **Google Sheets API**
   - **Google Drive API**

## مرحله 3: ایجاد Service Account

1. به "APIs & Services" > "Credentials" بروید
2. روی "Create Credentials" کلیک کنید
3. "Service Account" را انتخاب کنید
4. نام دلخواه بدهید (مثلاً "student-registration-service")
5. روی "Create and Continue" کلیک کنید
6. نقش "Editor" را انتخاب کنید
7. "Done" را بزنید

## مرحله 4: دانلود فایل JSON

1. روی Service Account ایجاد شده کلیک کنید
2. به تب "Keys" بروید
3. "Add Key" > "Create new key" را بزنید
4. فرمت "JSON" را انتخاب کنید
5. فایل JSON دانلود می‌شود
6. این فایل را با نام `google_credentials.json` در ریشه پروژه قرار دهید

## مرحله 5: ایجاد Google Sheet

1. به [Google Sheets](https://sheets.google.com) بروید
2. یک Sheet جدید بسازید
3. نام آن را `Student_Registrations` بگذارید
4. فایل JSON را باز کنید و ایمیل `client_email` را کپی کنید
5. Sheet را با این ایمیل به اشتراک بگذارید (با دسترسی Editor)

## مرحله 6: ایجاد پوشه در Google Drive

1. به [Google Drive](https://drive.google.com) بروید
2. یک پوشه جدید با نام `Student_Documents` بسازید
3. این پوشه را هم با ایمیل Service Account به اشتراک بگذارید

## مرحله 7: تنظیمات Django

فایل `.env` در ریشه پروژه بسازید:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
GOOGLE_SHEET_NAME=Student_Registrations
GOOGLE_DRIVE_FOLDER=Student_Documents
```

## مرحله 8: اجرای Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

## مرحله 9: تست سیستم

```bash
python manage.py runserver
```

به `http://127.0.0.1:8000/` بروید و فرم را تست کنید.

## ساختار Google Sheet

Sheet شما این ستون‌ها را خواهد داشت:

| ID | الاسم | الاسم بحسب الجواز | المقطع | التخصص | نوع الجامعة | جامعة البكالوريوس | جامعة الماجستير | رقم الهاتف | روابط الملفات... |

## نکات مهم

1. **امنیت**: فایل `google_credentials.json` را در `.gitignore` قرار دهید
2. **لینک‌های فایل**: تمام فایل‌ها در Drive ذخیره می‌شوند و لینک‌هاشون در Sheet قرار می‌گیرد
3. **ظرفیت**: برای 3000 دانشجو کاملاً مناسب است
4. **دسترسی**: می‌توانید Sheet را با تیم خود به اشتراک بگذارید

## مقیاس‌پذیری برای 3000 دانشجو

✅ **Google Sheets**: تا 10 میلیون سلول (کاملاً کافی)
✅ **Google Drive**: 15GB رایگان (برای فایل‌های PDF و تصاویر کافی است)
✅ **سرعت**: برای این حجم عالی است

## جایگزین‌ها (در صورت نیاز)

اگر حجم بیشتر شد:
- **Supabase**: دیتابیس PostgreSQL رایگان
- **AWS S3**: ذخیره‌سازی فایل
- **Backend اختصاصی**: Django + PostgreSQL + S3

ولی برای 3000 دانشجو، Google Sheets + Drive کاملاً مناسب و رایگان است! 🎉
