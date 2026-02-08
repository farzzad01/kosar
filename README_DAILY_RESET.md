# راهنمای ریست روزانه و گزارش‌گیری

## ویژگی‌های سیستم

### 1. ریست خودکار روزانه
- هر روز راس ساعت 12 شب، نوبت‌های روز قبل آرشیو می‌شوند
- تعداد رزروها در هر ساعت ریست می‌شود
- داده‌ها حذف نمی‌شوند، فقط آرشیو می‌شوند

### 2. گزارش‌گیری ماهانه
- تعداد کل نوبت‌ها در ماه
- تعداد دانشجویان ماجستیر و دکترا
- توزیع نوبت‌ها بر اساس ساعت

### 3. آرشیو روزانه
- ذخیره کامل اطلاعات هر روز
- قابل مشاهده در پنل ادمین

## نحوه اجرای ریست روزانه

### روش 1: اجرای دستی
```bash
python manage.py daily_reset
```

### روش 2: زمان‌بندی خودکار (Windows Task Scheduler)

1. باز کردن Task Scheduler
2. Create Basic Task
3. نام: "Django Daily Reset"
4. Trigger: Daily at 12:00 AM
5. Action: Start a program
   - Program: `C:\path\to\python.exe`
   - Arguments: `C:\path\to\manage.py daily_reset`
   - Start in: `C:\path\to\project`

### روش 3: استفاده از Cron (Linux/Mac)
```bash
crontab -e
```
اضافه کردن خط زیر:
```
0 0 * * * cd /path/to/project && /path/to/python manage.py daily_reset
```

## مشاهده گزارش‌ها در پنل ادمین

1. وارد پنل ادمین شوید: `http://localhost:8000/admin/`
2. بخش "التقارير الشهرية" (Monthly Reports)
3. بخش "الأرشيف اليومي" (Daily Archive)

## نکات مهم

- داده‌ها هرگز حذف نمی‌شوند
- فقط فیلد `is_archived` تغییر می‌کند
- گزارش‌ها به صورت JSON ذخیره می‌شوند
- می‌توانید گزارش‌ها را Export کنید
