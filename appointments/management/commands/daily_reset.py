from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from appointments.models import Appointment, DailyArchive, MonthlyReport
import json


class Command(BaseCommand):
    help = 'Archive daily appointments and reset for new day'

    def handle(self, *args, **options):
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        
        # Get yesterday's appointments
        yesterday_appointments = Appointment.objects.filter(
            appointment_date=yesterday,
            is_archived=False
        )
        
        if yesterday_appointments.exists():
            # Prepare data for archive
            appointments_data = []
            for apt in yesterday_appointments:
                appointments_data.append({
                    'name': apt.name,
                    'phone': apt.phone,
                    'degree': apt.degree,
                    'appointment_time': apt.appointment_time,
                    'reason': apt.reason,
                    'duration': apt.duration,
                    'created_at': apt.created_at.isoformat(),
                })
            
            # Create daily archive
            DailyArchive.objects.create(
                archive_date=yesterday,
                appointments_data=appointments_data,
                total_count=len(appointments_data)
            )
            
            # Mark as archived
            yesterday_appointments.update(is_archived=True)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully archived {len(appointments_data)} appointments from {yesterday}'
                )
            )
            
            # Update monthly report
            self.update_monthly_report(yesterday, yesterday_appointments)
        else:
            self.stdout.write(
                self.style.WARNING(f'No appointments found for {yesterday}')
            )

    def update_monthly_report(self, date, appointments):
        # Get or create monthly report
        month_start = date.replace(day=1)
        report, created = MonthlyReport.objects.get_or_create(
            month=month_start,
            defaults={
                'total_appointments': 0,
                'master_count': 0,
                'phd_count': 0,
                'time_slot_data': {}
            }
        )
        
        # Count by degree
        master_count = appointments.filter(degree='master').count()
        phd_count = appointments.filter(degree='phd').count()
        
        # Count by time slot
        time_slot_data = report.time_slot_data or {}
        for apt in appointments:
            time = apt.appointment_time
            time_slot_data[time] = time_slot_data.get(time, 0) + 1
        
        # Update report
        report.total_appointments += appointments.count()
        report.master_count += master_count
        report.phd_count += phd_count
        report.time_slot_data = time_slot_data
        report.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'Updated monthly report for {month_start.strftime("%Y-%m")}')
        )
