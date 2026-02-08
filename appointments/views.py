from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from django.http import JsonResponse
from .forms import AppointmentForm
from .models import Appointment

def home(request):
    today = timezone.now().date()
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم حجز موعدك بنجاح! في انتظار حضورك')
            return redirect('home')
    else:
        form = AppointmentForm()
    
    # Get count of today's appointments per hour slot
    time_counts = {}
    time_slots = [
        ('19:00', '7 مساءً'),
        ('20:00', '8 مساءً'),
        ('21:00', '9 مساءً'),
        ('22:00', '10 مساءً'),
        ('23:00', '11 مساءً'),
        ('00:00', '12 منتصف الليل'),
    ]
    
    for time, label in time_slots:
        # Count all appointments in this hour (19:00, 19:10, 19:20, etc.)
        hour = time.split(':')[0]
        count = Appointment.objects.filter(
            appointment_date=today,
            appointment_time__startswith=hour,
            is_archived=False
        ).count()
        time_counts[time] = count
    
    context = {
        'form': form,
        'time_slots': time_slots,
        'time_counts': time_counts,
    }
    
    return render(request, 'home.html', context)


def get_occupied_slots(request):
    """API endpoint to get occupied time slots for a specific date and hour"""
    date = request.GET.get('date')
    hour = request.GET.get('hour')
    
    if not date or not hour:
        return JsonResponse({'error': 'Missing parameters'}, status=400)
    
    # Get all appointments for this date and hour
    occupied = Appointment.objects.filter(
        appointment_date=date,
        appointment_time__startswith=hour,
        is_archived=False
    ).values_list('appointment_time', flat=True)
    
    return JsonResponse({'occupied': list(occupied)})

