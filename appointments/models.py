from django.db import models

class Appointment(models.Model):
    DEGREE_CHOICES = [
        ('master', 'ماجستير'),
        ('phd', 'دكتوراه'),
    ]
    
    TIME_CHOICES = [
        ('19:00', '19:00 - 7 مساءً'),
        ('20:00', '20:00 - 8 مساءً'),
        ('21:00', '21:00 - 9 مساءً'),
        ('22:00', '22:00 - 10 مساءً'),
        ('23:00', '23:00 - 11 مساءً'),
        ('00:00', '00:00 - 12 منتصف الليل'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="الاسم الكامل")
    phone = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    degree = models.CharField(max_length=10, choices=DEGREE_CHOICES, verbose_name="المرحلة الدراسية")
    appointment_date = models.DateField(verbose_name="تاريخ الموعد")
    appointment_time = models.CharField(max_length=5, choices=TIME_CHOICES, verbose_name="ساعة الحضور")
    reason = models.TextField(verbose_name="دليل المراجعة")
    duration = models.CharField(max_length=50, verbose_name="مدة الحضور")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الحجز")
    is_archived = models.BooleanField(default=False, verbose_name="مؤرشف")

    class Meta:
        ordering = ['appointment_date', 'appointment_time']
        verbose_name = "موعد"
        verbose_name_plural = "المواعيد"

    def __str__(self):
        return f"{self.name} - {self.appointment_date} {self.appointment_time}"


class MonthlyReport(models.Model):
    month = models.DateField(verbose_name="الشهر")
    total_appointments = models.IntegerField(default=0, verbose_name="إجمالي المواعيد")
    master_count = models.IntegerField(default=0, verbose_name="عدد طلاب الماجستير")
    phd_count = models.IntegerField(default=0, verbose_name="عدد طلاب الدكتوراه")
    time_slot_data = models.JSONField(default=dict, verbose_name="بيانات الأوقات")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    class Meta:
        ordering = ['-month']
        verbose_name = "تقرير شهري"
        verbose_name_plural = "التقارير الشهرية"

    def __str__(self):
        return f"تقرير {self.month.strftime('%Y-%m')}"


class DailyArchive(models.Model):
    archive_date = models.DateField(verbose_name="تاريخ الأرشيف")
    appointments_data = models.JSONField(verbose_name="بيانات المواعيد")
    total_count = models.IntegerField(default=0, verbose_name="العدد الإجمالي")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    class Meta:
        ordering = ['-archive_date']
        verbose_name = "أرشيف يومي"
        verbose_name_plural = "الأرشيف اليومي"

    def __str__(self):
        return f"أرشيف {self.archive_date}"
