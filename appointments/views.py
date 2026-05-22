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
        phone = request.POST.get('phone', '')
        address_iraq = request.POST.get('address_iraq', '')
        job = request.POST.get('job', '')
        marital_status = request.POST.get('marital_status', '')
        children_count = request.POST.get('children_count', None)
        
        university_type = request.POST.get('university_type', '')
        degree = request.POST.get('degree', '')
        major = request.POST.get('major', '')
        bachelor_gpa = request.POST.get('bachelor_gpa', '')
        master_gpa = request.POST.get('master_gpa', '')
        
        print(f"Received data: {name}, {degree}, {phone}")
        
        # Get uploaded files
        passport = request.FILES.get('passport')
        transcript = request.FILES.get('transcript')
        university_form = request.FILES.get('university_form')
        
        # Create file URLs (just filenames for now)
        file_urls = {
            'passport_url': passport.name if passport else '',
            'transcript_url': transcript.name if transcript else '',
            'university_form_url': university_form.name if university_form else ''
        }
        
        # Create database record
        registration = StudentRegistration.objects.create(
            name=name,
            passport_name=passport_name,
            phone=phone,
            address_iraq=address_iraq,
            job=job,
            marital_status=marital_status,
            children_count=int(children_count) if children_count else None,
            university_type=university_type,
            degree=degree,
            major=major,
            bachelor_gpa=bachelor_gpa,
            master_gpa=master_gpa if master_gpa else None,
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
                phone,
                address_iraq,
                job,
                marital_status,
                str(children_count) if children_count else '',
                university_type,
                degree_display,
                major,
                bachelor_gpa,
                master_gpa if master_gpa else '',
                file_urls.get('passport_url', ''),
                file_urls.get('transcript_url', ''),
                file_urls.get('university_form_url', ''),
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
