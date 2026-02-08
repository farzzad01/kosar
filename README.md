# سامانه نوبت‌دهی دکتر تقی‌زاده

سیستم مدیریت نوبت‌دهی برای مشاوره‌های دانشجویی در رشته حقوق (ماجستیر و دکترا)

## ویژگی‌ها

✅ فرم ثبت نوبت با انتخاب ساعت (7 شب تا 12 شب)
✅ نمایش تعداد رزروها در هر ساعت
✅ پنل مدیریت Django
✅ گزارش‌گیری روزانه و ماهانه
✅ ریست خودکار روزانه
✅ رابط کاربری زیبا با Tailwind CSS
✅ پشتیبانی از زبان عربی

## نصب و راه‌اندازی محلی

### پیش‌نیازها
- Python 3.11+
- pip

### مراحل نصب

1. کلون کردن پروژه:
```bash
git clone <repository-url>
cd reserve_kosar
```

2. نصب وابستگی‌ها:
```bash
pip install -r requirements.txt
```

3. اجرای migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. ایجاد superuser:
```bash
python manage.py createsuperuser
```

5. اجرای سرور:
```bash
python manage.py runserver
```

6. باز کردن در مرورگر:
- صفحه اصلی: http://127.0.0.1:8000/
- پنل ادمین: http://127.0.0.1:8000/admin/

## استفاده

### ثبت نوبت
1. وارد صفحه اصلی شوید
2. فرم را پر کنید:
   - نام کامل
   - شماره تلفن
   - مرحله تحصیلی (ماجستیر/دکترا)
   - تاریخ نوبت
   - ساعت حضور (کلیک روی مربع‌ها)
   - دلیل مراجعه
   - مدت زمان حضور
3. روی "تأکید الحجز" کلیک کنید

### مدیریت نوبت‌ها
1. وارد پنل ادمین شوید
2. بخش "المواعيد" (Appointments):
   - مشاهده تمام نوبت‌ها
   - جستجو و فیلتر
   - ویرایش و حذف
3. بخش "التقارير الشهرية" (Monthly Reports):
   - گزارش‌های ماهانه
   - آمار دانشجویان
   - توزیع ساعات
4. بخش "الأرشيف اليومي" (Daily Archive):
   - آرشیو روزانه نوبت‌ها

### ریست روزانه
برای آرشیو کردن نوبت‌های روز قبل:
```bash
python manage.py daily_reset
```

## دیپلوی

برای دیپلوی روی Render.com، فایل [DEPLOY_GUIDE.md](DEPLOY_GUIDE.md) را مطالعه کنید.

## ساختار پروژه

```
reserve_kosar/
├── appointments/          # اپلیکیشن اصلی
│   ├── models.py         # مدل‌های دیتابیس
│   ├── views.py          # ویوها
│   ├── forms.py          # فرم‌ها
│   ├── admin.py          # تنظیمات پنل ادمین
│   └── management/       # دستورات مدیریتی
├── templates/            # تمپلیت‌های HTML
├── static/              # فایل‌های استاتیک
├── nobatdehi/           # تنظیمات پروژه
└── manage.py
```

## تکنولوژی‌ها

- **Backend**: Django 4.2
- **Database**: SQLite (محلی) / PostgreSQL (production)
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Deployment**: Render.com

## مجوز

این پروژه برای استفاده شخصی و آموزشی است.
