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
        
        print(f"Received data: {name}, {degree}, {phone}")
        
        # Get uploaded files
        passport = request.FILES.get('passport')
        bachelor_cert = request.FILES.get('bachelor_cert')
        master_cert = request.FILES.get('master_cert')
        bachelor_transcript = request.FILES.get('bachelor_transcript')
        master_transcript = request.FILES.get('master_transcript')
        filled_form = request.FILES.get('filled_form')
        
        # Create file URLs (just filenames for now)
        file_urls = {
            'passport_url': passport.name if passport else '',
            'bachelor_cert_url': bachelor_cert.name if bachelor_cert else '',
            'master_cert_url': master_cert.name if master_cert else '',
            'bachelor_transcript_url': bachelor_transcript.name if bachelor_transcript else '',
            'master_transcript_url': master_transcript.name if master_transcript else '',
            'filled_form_url': filled_form.name if filled_form else ''
        }
        
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
        
        print(f"Registration created with ID: {registration.id}")
        
        # Send to Google Sheets
        try:
            sheets_service = GoogleSheetsService()
            
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
            
            row_number = sheets_service.add_row(row_data)
            registration.google_sheet_row = row_number
            registration.save()
            
            print(f"Data added to Google Sheets at row {row_number}")
        except Exception as sheet_error:
            print(f"Google Sheets error (continuing anyway): {str(sheet_error)}")
            print(traceback.format_exc())
        
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
