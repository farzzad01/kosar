from django.db import models

class Appointment(models.Model):
    DEGREE_CHOICES = [
        ('master', 'کارشناسی ارشد'),
        ('phd', 'دکترا'),
    ]
    
    TIME_CHOICES = [
        ('19:00', '19:00 - 7 عصر'),
        ('20:00', '20:00 - 8 شب'),
        ('21:00', '21:00 - 9 شب'),
        ('22:00', '22:00 - 10 شب'),
        ('23:00', '23:00 - 11 شب'),
        ('00:00', '00:00 - 12 نیمه شب'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="نام کامل")
    phone = models.CharField(max_length=20, verbose_name="شماره تلفن")
    degree = models.CharField(max_length=10, choices=DEGREE_CHOICES, verbose_name="مقطع تحصیلی")
    appointment_date = models.DateField(verbose_name="تاریخ نوبت")
    appointment_time = models.CharField(max_length=5, choices=TIME_CHOICES, verbose_name="ساعت حضور")
    reason = models.TextField(verbose_name="دلیل مراجعه")
    duration = models.CharField(max_length=50, verbose_name="مدت حضور")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    is_archived = models.BooleanField(default=False, verbose_name="بایگانی شده")

    class Meta:
        ordering = ['appointment_date', 'appointment_time']
        verbose_name = "نوبت"
        verbose_name_plural = "نوبت‌ها"

    def __str__(self):
        return f"{self.name} - {self.appointment_date} {self.appointment_time}"


class MonthlyReport(models.Model):
    month = models.DateField(verbose_name="ماه")
    total_appointments = models.IntegerField(default=0, verbose_name="مجموع نوبت‌ها")
    master_count = models.IntegerField(default=0, verbose_name="تعداد دانشجویان ارشد")
    phd_count = models.IntegerField(default=0, verbose_name="تعداد دانشجویان دکترا")
    time_slot_data = models.JSONField(default=dict, verbose_name="داده‌های زمانی")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        ordering = ['-month']
        verbose_name = "گزارش ماهانه"
        verbose_name_plural = "گزارش‌های ماهانه"

    def __str__(self):
        return f"گزارش {self.month.strftime('%Y-%m')}"


class DailyArchive(models.Model):
    archive_date = models.DateField(verbose_name="تاریخ بایگانی")
    appointments_data = models.JSONField(verbose_name="داده‌های نوبت‌ها")
    total_count = models.IntegerField(default=0, verbose_name="تعداد کل")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        ordering = ['-archive_date']
        verbose_name = "بایگانی روزانه"
        verbose_name_plural = "بایگانی‌های روزانه"

    def __str__(self):
        return f"بایگانی {self.archive_date}"
