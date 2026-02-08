from django.contrib import admin
from .models import Appointment, MonthlyReport, DailyArchive

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'degree', 'appointment_date', 'appointment_time', 'is_archived', 'created_at')
    list_filter = ('degree', 'appointment_date', 'appointment_time', 'is_archived')
    search_fields = ('name', 'phone', 'reason')
    readonly_fields = ('created_at',)
    ordering = ('-appointment_date', '-appointment_time')
    
    fieldsets = (
        ('معلومات الطالب', {
            'fields': ('name', 'phone', 'degree')
        }),
        ('تفاصيل الموعد', {
            'fields': ('appointment_date', 'appointment_time', 'duration')
        }),
        ('تفاصيل الاستشارة', {
            'fields': ('reason', 'created_at', 'is_archived')
        }),
    )


@admin.register(MonthlyReport)
class MonthlyReportAdmin(admin.ModelAdmin):
    list_display = ('month', 'total_appointments', 'master_count', 'phd_count', 'created_at')
    list_filter = ('month',)
    readonly_fields = ('created_at',)
    ordering = ('-month',)
    
    fieldsets = (
        ('معلومات التقرير', {
            'fields': ('month', 'total_appointments', 'master_count', 'phd_count')
        }),
        ('بيانات الأوقات', {
            'fields': ('time_slot_data', 'created_at')
        }),
    )


@admin.register(DailyArchive)
class DailyArchiveAdmin(admin.ModelAdmin):
    list_display = ('archive_date', 'total_count', 'created_at')
    list_filter = ('archive_date',)
    readonly_fields = ('created_at',)
    ordering = ('-archive_date',)
    
    fieldsets = (
        ('معلومات الأرشيف', {
            'fields': ('archive_date', 'total_count', 'created_at')
        }),
        ('البيانات', {
            'fields': ('appointments_data',)
        }),
    )
