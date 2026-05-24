from django.contrib import admin
from .models import StudentRegistration

@admin.register(StudentRegistration)
class StudentRegistrationAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_full_name', 'degree', 'major', 'phone', 'email', 'created_at']
    list_filter = ['degree', 'university_type', 'religion', 'marital_status', 'created_at']
    search_fields = ['first_name', 'middle_name', 'last_name', 'phone', 'email', 'major']
    readonly_fields = ['created_at', 'google_sheet_row']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.middle_name} {obj.last_name}"
    get_full_name.short_description = 'الاسم الكامل'
    
    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('first_name', 'middle_name', 'last_name', 'religion', 'phone', 'email', 
                      'address_iraq', 'job', 'marital_status', 'children_count')
        }),
        ('المعلومات الأكاديمية', {
            'fields': ('degree', 'major', 'university_type', 'previous_university', 
                      'bachelor_gpa', 'master_gpa')
        }),
        ('روابط المستندات', {
            'fields': ('passport_url', 'transcript_url', 'master_transcript_url', 'university_form_url')
        }),
        ('معلومات النظام', {
            'fields': ('created_at', 'google_sheet_row')
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion to keep data integrity with Google Sheets
        return request.user.is_superuser
