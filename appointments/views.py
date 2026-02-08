from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from .forms import AppointmentForm
from .models import Appointment

def home(request):
    today = timezone.now().date()
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم حجز موعدك بنجاح! سنتواصل معك قريباً.')
            return redirect('home')
    else:
        form = AppointmentForm()
    
    # Get count of today's appointments per time slot
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
        count = Appointment.objects.filter(
            appointment_date=today,
            appointment_time=time,
            is_archived=False
        ).count()
        time_counts[time] = count
    
    context = {
        'form': form,
        'time_slots': time_slots,
        'time_counts': time_counts,
    }
    
    return render(request, 'home.html', context)
