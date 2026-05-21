from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import StudentRegistration
from .google_sheets_service import GoogleSheetsService
from datetime import datetime

def registration(request):
    """Registration form page"""
    return render(request, 'registration.html')


@csrf_exempt
def submit_registration(request):
    """Handle registration form submission"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
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
        
        # Get uploaded files
        passport = request.FILES.get('passport')
        bachelor_cert = request.FILES.get('bachelor_cert')
        master_cert = request.FILES.get('master_cert')
        bachelor_transcript = request.FILES.get('bachelor_transcript')
        master_transcript = request.FILES.get('master_transcript')
        filled_form = request.FILES.get('filled_form')
        
        # Initialize Google Sheets service
        sheets_service = GoogleSheetsService()
        
        # Upload files and get URLs (placeholder for now)
        file_urls = {}
        if passport:
            file_urls['passport_url'] = sheets_service.upload_to_drive(passport, f"passport_{name}")
        if bachelor_cert:
            file_urls['bachelor_cert_url'] = sheets_service.upload_to_drive(bachelor_cert, f"bachelor_cert_{name}")
        if master_cert:
            file_urls['master_cert_url'] = sheets_service.upload_to_drive(master_cert, f"master_cert_{name}")
        if bachelor_transcript:
            file_urls['bachelor_transcript_url'] = sheets_service.upload_to_drive(bachelor_transcript, f"bachelor_transcript_{name}")
        if master_transcript:
            file_urls['master_transcript_url'] = sheets_service.upload_to_drive(master_transcript, f"master_transcript_{name}")
        if filled_form:
            file_urls['filled_form_url'] = sheets_service.upload_to_drive(filled_form, f"filled_form_{name}")
        
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
            **file_urls
        )
        
        # Prepare data for Google Sheets
        degree_display = 'ماجستير' if degree == 'master' else 'دكتوراه'
        row_data = [
            str(registration.id),
            name,
            passport_name,
            degree_display,
            major,
            university_type,
            bachelor_university,
            master_university,
            phone,
            file_urls.get('passport_url', ''),
            file_urls.get('bachelor_cert_url', ''),
            file_urls.get('master_cert_url', ''),
            file_urls.get('bachelor_transcript_url', ''),
            file_urls.get('master_transcript_url', ''),
            file_urls.get('filled_form_url', ''),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ]
        
        # Add to Google Sheets
        row_number = sheets_service.add_row(row_data)
        registration.google_sheet_row = row_number
        registration.save()
        
        return JsonResponse({
            'success': True,
            'message': 'تم إرسال طلبك بنجاح!',
            'registration_id': registration.id
        })
        
    except Exception as e:
        print(f"Error in submit_registration: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
