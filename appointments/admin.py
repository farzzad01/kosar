from django.contrib import admin
from .models import StudentRegistration

@admin.register(StudentRegistration)
class StudentRegistrationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'passport_name', 'degree', 'major', 'phone', 'created_at']
    list_filter = ['degree', 'university_type', 'created_at']
    search_fields = ['name', 'passport_name', 'phone', 'major']
    readonly_fields = ['created_at', 'google_sheet_row']
    
    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('name', 'passport_name', 'phone')
        }),
        ('المعلومات الأكاديمية', {
            'fields': ('degree', 'major', 'university_type', 'bachelor_university', 'master_university')
        }),
        ('روابط المستندات', {
            'fields': ('passport_url', 'bachelor_cert_url', 'master_cert_url', 
                      'bachelor_transcript_url', 'master_transcript_url', 'filled_form_url')
        }),
        ('معلومات النظام', {
            'fields': ('created_at', 'google_sheet_row')
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion to keep data integrity with Google Sheets
        return request.user.is_superuser
