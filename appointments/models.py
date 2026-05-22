from django.db import models

class StudentRegistration(models.Model):
    DEGREE_CHOICES = [
        ('master', 'ماجستير'),
        ('phd', 'دكتوراه'),
    ]
    
    UNIVERSITY_TYPE_CHOICES = [
        ('نفقة خاصة', 'نفقة خاصة'),
        ('ابتعاث', 'ابتعاث'),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('مجرد', 'مجرد'),
        ('متأهل', 'متأهل'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200, verbose_name="الاسم")
    passport_name = models.CharField(max_length=200, verbose_name="الاسم بحسب الجواز")
    phone = models.CharField(max_length=30, verbose_name="رقم الهاتف")
    address_iraq = models.CharField(max_length=300, default='', verbose_name="العنوان في العراق")
    job = models.CharField(max_length=200, default='', verbose_name="الوظيفة")
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, default='مجرد', verbose_name="الحالة الاجتماعية")
    children_count = models.IntegerField(blank=True, null=True, verbose_name="عدد الأطفال")
    
    # Academic Information
    university_type = models.CharField(max_length=50, choices=UNIVERSITY_TYPE_CHOICES, verbose_name="نوع الجامعة")
    degree = models.CharField(max_length=10, choices=DEGREE_CHOICES, verbose_name="المقطع")
    major = models.CharField(max_length=200, verbose_name="التخصص")
    bachelor_gpa = models.CharField(max_length=50, default='', verbose_name="معدل البكالوريوس")
    master_gpa = models.CharField(max_length=50, blank=True, null=True, verbose_name="معدل الماجستير")
    
    # File URLs (stored in Google Drive)
    passport_url = models.URLField(blank=True, null=True, verbose_name="رابط عکس پاسپورت")
    transcript_url = models.URLField(blank=True, null=True, verbose_name="رابط كشف درجات")
    university_form_url = models.URLField(blank=True, null=True, verbose_name="رابط استمارة التحصيل الجامعي")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التسجيل")
    google_sheet_row = models.IntegerField(blank=True, null=True, verbose_name="رقم الصف في الشيت")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "تسجيل طالب"
        verbose_name_plural = "تسجيلات الطلاب"
    
    def __str__(self):
        return f"{self.name} - {self.get_degree_display()}"
