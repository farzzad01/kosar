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
        ('اطلاعات دانشجو', {
            'fields': ('name', 'phone', 'degree')
        }),
        ('جزئیات نوبت', {
            'fields': ('appointment_date', 'appointment_time', 'duration')
        }),
        ('جزئیات مشاوره', {
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
        ('اطلاعات گزارش', {
            'fields': ('month', 'total_appointments', 'master_count', 'phd_count')
        }),
        ('داده‌های زمانی', {
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
        ('اطلاعات بایگانی', {
            'fields': ('archive_date', 'total_count', 'created_at')
        }),
        ('داده‌ها', {
            'fields': ('appointments_data',)
        }),
    )
