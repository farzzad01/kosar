from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import StudentRegistration
from .google_sheets_service import GoogleSheetsService
from datetime import datetime
import traceback

def registration(request):
    """Registration form page"""
    return render(request, 'registration.html')


@require_http_methods(["POST"])
def submit_registration(request):
    """Handle registration form submission"""
    try:
        # Get form data
        name = request.POST.get('name', '')
        passport_name = request.POST.get('passport_name', '')
        degree = request.POST.get('degree', '')
        major = request.POST.get('major', '')
        university_type = request.POST.get('university_type', '')
        bachelor_university = request.POST.get('bachelor_university', '')
        master_university = request.POST.get('master_university', '')
        phone = request.POST.get('phone', '')
        
        print(f"Received data: {name}, {degree}, {phone}")  # Debug
        
        # Get uploaded files
        passport = request.FILES.get('passport')
        bachelor_cert = request.FILES.get('bachelor_cert')
        master_cert = request.FILES.get('master_cert')
        bachelor_transcript = request.FILES.get('bachelor_transcript')
        master_transcript = request.FILES.get('master_transcript')
        filled_form = request.FILES.get('filled_form')
        
        print(f"Files received: passport={passport}, bachelor_cert={bachelor_cert}")  # Debug
        
        # For now, save to database without Google Sheets (for testing)
        # Create database record
        registration = StudentRegistration.objects.create(
            name=name,
            passport_name=passport_name,
            degree=degree,
            major=major,
            university_type=university_type,
            bachelor_university=bachelor_university,
            master_university=master_university,
            phone=phone,
            passport_url=f"File: {passport.name if passport else 'None'}",
            bachelor_cert_url=f"File: {bachelor_cert.name if bachelor_cert else 'None'}",
            master_cert_url=f"File: {master_cert.name if master_cert else 'None'}",
            bachelor_transcript_url=f"File: {bachelor_transcript.name if bachelor_transcript else 'None'}",
            master_transcript_url=f"File: {master_transcript.name if master_transcript else 'None'}",
            filled_form_url=f"File: {filled_form.name if filled_form else 'None'}"
        )
        
        print(f"Registration created with ID: {registration.id}")  # Debug
        
        return JsonResponse({
            'success': True,
            'message': 'تم إرسال طلبك بنجاح!',
            'registration_id': registration.id
        })
        
    except Exception as e:
        print(f"Error in submit_registration: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
