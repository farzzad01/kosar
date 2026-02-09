# راهنمای نصب Supabase

## مرحله 1: ساخت دیتابیس Supabase

1. برو به https://supabase.com
2. ثبت‌نام کن (رایگان)
3. یک پروژه جدید بساز
4. از منوی سمت چپ، برو به **Settings** > **Database**
5. Connection String رو کپی کن (URI format)

مثال:
```
postgresql://postgres.xxxxx:password@aws-0-region.pooler.supabase.com:5432/postgres
```

## مرحله 2: تنظیم Environment Variables در Vercel

1. برو به https://vercel.com/dashboard
2. پروژه kosar رو باز کن
3. برو به **Settings** > **Environment Variables**
4. این متغیرها رو اضافه کن:

```
DATABASE_URL = postgresql://postgres.xxxxx:password@...
SECRET_KEY = یک کلید تصادفی طولانی
DEBUG = False
```

برای ساخت SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## مرحله 3: دیپلوی

بعد از اضافه کردن متغیرها، Vercel خودکار دوباره دیپلوی می‌کنه.

## مرحله 4: دسترسی به پنل ادمین

1. URL پنل ادمین: `https://kosar-seven.vercel.app/secret-admin-panel-xyz/`
2. برای ساخت superuser، باید از Vercel CLI استفاده کنی:

```bash
vercel env pull
python manage.py createsuperuser
```

یا از Supabase SQL Editor:
```sql
INSERT INTO auth_user (username, password, is_superuser, is_staff, is_active, date_joined)
VALUES ('admin', 'pbkdf2_sha256$...', true, true, true, NOW());
```

## نکات امنیتی:

- ✅ URL پنل ادمین تغییر کرده: `/secret-admin-panel-xyz/`
- ✅ DEBUG=False در production
- ✅ SECRET_KEY در environment variable
- ✅ PostgreSQL به جای SQLite
- ⚠️ حتما پسورد قوی برای admin استفاده کن
- ⚠️ URL پنل ادمین رو با کسی به اشتراک نذار

## مشاهده داده‌ها:

دو راه داری:
1. پنل ادمین Django: `https://kosar-seven.vercel.app/secret-admin-panel-xyz/`
2. پنل Supabase: https://supabase.com/dashboard (Table Editor)
