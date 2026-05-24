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
        ('أعزب', 'أعزب'),
        ('متزوج', 'متزوج'),
    ]
    
    # Basic Information
    first_name = models.CharField(max_length=100, default='', verbose_name="الاسم الأول")
    middle_name = models.CharField(max_length=200, default='', verbose_name="الاسم الثلاثي")
    last_name = models.CharField(max_length=100, default='', verbose_name="لقب العائلة")
    religion = models.CharField(max_length=50, default='', verbose_name="الديانة")
    phone = models.CharField(max_length=30, default='', verbose_name="رقم الهاتف")
    email = models.EmailField(default='', verbose_name="البريد الإلكتروني")
    address_iraq = models.CharField(max_length=300, default='', verbose_name="العنوان في العراق")
    job = models.CharField(max_length=200, default='', verbose_name="الوظيفة")
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, default='أعزب', verbose_name="الحالة الاجتماعية")
    children_count = models.IntegerField(blank=True, null=True, verbose_name="عدد الأطفال")
    
    # Academic Information
    university_type = models.CharField(max_length=50, choices=UNIVERSITY_TYPE_CHOICES, verbose_name="نوع الجامعة")
    degree = models.CharField(max_length=10, choices=DEGREE_CHOICES, verbose_name="المقطع")
    major = models.CharField(max_length=200, verbose_name="التخصص")
    previous_university = models.CharField(max_length=300, default='', verbose_name="الجامعة السابقة")
    bachelor_gpa = models.CharField(max_length=50, default='', verbose_name="معدل البكالوريوس")
    master_gpa = models.CharField(max_length=50, blank=True, null=True, verbose_name="معدل الماجستير")
    
    # File URLs (stored in Google Drive)
    passport_url = models.URLField(blank=True, null=True, verbose_name="رابط عکس پاسپورت")
    transcript_url = models.URLField(blank=True, null=True, verbose_name="رابط كشف درجات البكالوريوس")
    master_transcript_url = models.URLField(blank=True, null=True, verbose_name="رابط كشف درجات الماجستير")
    university_form_url = models.URLField(blank=True, null=True, verbose_name="رابط استمارة التحصيل الجامعي")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التسجيل")
    google_sheet_row = models.IntegerField(blank=True, null=True, verbose_name="رقم الصف في الشيت")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "تسجيل طالب"
        verbose_name_plural = "تسجيلات الطلاب"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_degree_display()}"
