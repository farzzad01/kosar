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
    
    # Basic Information
    name = models.CharField(max_length=200, verbose_name="الاسم")
    passport_name = models.CharField(max_length=200, verbose_name="الاسم بحسب الجواز")
    degree = models.CharField(max_length=10, choices=DEGREE_CHOICES, verbose_name="المقطع")
    major = models.CharField(max_length=200, verbose_name="التخصص")
    university_type = models.CharField(max_length=50, choices=UNIVERSITY_TYPE_CHOICES, verbose_name="نوع الجامعة")
    bachelor_university = models.CharField(max_length=200, verbose_name="جامعة البكالوريوس")
    master_university = models.CharField(max_length=200, blank=True, null=True, verbose_name="جامعة الماجستير")
    phone = models.CharField(max_length=30, verbose_name="رقم الهاتف")
    
    # File URLs (stored in Google Drive)
    passport_url = models.URLField(blank=True, null=True, verbose_name="رابط جواز السفر")
    bachelor_cert_url = models.URLField(blank=True, null=True, verbose_name="رابط شهادة البكالوريوس")
    master_cert_url = models.URLField(blank=True, null=True, verbose_name="رابط شهادة الماجستير")
    bachelor_transcript_url = models.URLField(blank=True, null=True, verbose_name="رابط كشف درجات البكالوريوس")
    master_transcript_url = models.URLField(blank=True, null=True, verbose_name="رابط كشف درجات الماجستير")
    filled_form_url = models.URLField(blank=True, null=True, verbose_name="رابط الاستمارة المعبأة")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التسجيل")
    google_sheet_row = models.IntegerField(blank=True, null=True, verbose_name="رقم الصف في الشيت")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "تسجيل طالب"
        verbose_name_plural = "تسجيلات الطلاب"
    
    def __str__(self):
        return f"{self.name} - {self.get_degree_display()}"
