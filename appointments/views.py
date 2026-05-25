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
        # Validate required fields
        required_fields = {
            'first_name': 'الاسم الأول',
            'middle_name': 'الاسم الثلاثي',
            'last_name': 'اسم العائلة',
            'religion': 'الديانة',
            'phone': 'رقم الهاتف',
            'email': 'البريد الإلكتروني',
            'address_iraq': 'العنوان',
            'job': 'الوظيفة',
            'marital_status': 'الحالة الاجتماعية',
            'university_type': 'نوع الجامعة',
            'degree': 'المقطع الدراسي',
            'major': 'التخصص',
            'previous_university': 'الجامعة السابقة',
            'bachelor_gpa': 'معدل البكالوريوس'
        }
        
        missing_fields = []
        for field, label in required_fields.items():
            if not request.POST.get(field):
                missing_fields.append(label)
        
        if missing_fields:
            return JsonResponse({
                'success': False,
                'error': f'الحقول المطلوبة مفقودة: {", ".join(missing_fields)}'
            }, status=400)
        
        # Validate required files
        required_files = {
            'passport': 'صورة جواز السفر',
            'transcript': 'كشف درجات البكالوريوس',
            'university_form': 'استمارة التحصيل الجامعي'
        }
        
        missing_files = []
        for field, label in required_files.items():
            if not request.FILES.get(field):
                missing_files.append(label)
        
        # Check for PhD specific requirements
        degree = request.POST.get('degree', '')
        if degree == 'phd':
            if not request.POST.get('master_gpa'):
                missing_fields.append('معدل الماجستير')
            if not request.FILES.get('master_transcript'):
                missing_files.append('كشف درجات الماجستير')
        
        if missing_files:
            return JsonResponse({
                'success': False,
                'error': f'الملفات المطلوبة مفقودة: {", ".join(missing_files)}'
            }, status=400)
        
        # Get form data
        first_name = request.POST.get('first_name', '')
        middle_name = request.POST.get('middle_name', '')
        last_name = request.POST.get('last_name', '')
        religion = request.POST.get('religion', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        address_iraq = request.POST.get('address_iraq', '')
        job = request.POST.get('job', '')
        marital_status = request.POST.get('marital_status', '')
        children_count = request.POST.get('children_count', None)
        
        university_type = request.POST.get('university_type', '')
        major = request.POST.get('major', '')
        previous_university = request.POST.get('previous_university', '')
        bachelor_gpa = request.POST.get('bachelor_gpa', '')
        master_gpa = request.POST.get('master_gpa', '')
        
        print(f"[DEBUG] Received data: {first_name} {last_name}, {degree}, {phone}")
        
        # Get uploaded files
        passport = request.FILES.get('passport')
        transcript = request.FILES.get('transcript')
        master_transcript = request.FILES.get('master_transcript')
        university_form = request.FILES.get('university_form')
        
        # Create file URLs (just filenames for now)
        file_urls = {
            'passport_url': passport.name if passport else '',
            'transcript_url': transcript.name if transcript else '',
            'master_transcript_url': master_transcript.name if master_transcript else '',
            'university_form_url': university_form.name if university_form else ''
        }
        
        print(f"[DEBUG] Files received: {list(file_urls.keys())}")
        
        # Create database record
        try:
            registration = StudentRegistration.objects.create(
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                religion=religion,
                phone=phone,
                email=email,
                address_iraq=address_iraq,
                job=job,
                marital_status=marital_status,
                children_count=int(children_count) if children_count else None,
                university_type=university_type,
                degree=degree,
                major=major,
                previous_university=previous_university,
                bachelor_gpa=bachelor_gpa,
                master_gpa=master_gpa if master_gpa else None,
                **file_urls
            )
            print(f"[DEBUG] Registration created with ID: {registration.id}")
        except Exception as db_error:
            print(f"[ERROR] Database error: {str(db_error)}")
            return JsonResponse({
                'success': False,
                'error': f'خطأ في قاعدة البيانات: {str(db_error)}'
            }, status=500)
        
        # Send to Google Sheets
        sheets_error = None
        try:
            sheets_service = GoogleSheetsService()
            
            degree_display = 'ماجستير' if degree == 'master' else 'دكتوراه'
            full_name = f"{first_name} {middle_name} {last_name}"
            row_data = [
                str(registration.id),
                full_name,
                religion,
                phone,
                email,
                address_iraq,
                job,
                marital_status,
                str(children_count) if children_count else '',
                university_type,
                degree_display,
                major,
                previous_university,
                bachelor_gpa,
                master_gpa if master_gpa else '',
                file_urls.get('passport_url', ''),
                file_urls.get('transcript_url', ''),
                file_urls.get('master_transcript_url', ''),
                file_urls.get('university_form_url', ''),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ]
            
            row_number = sheets_service.add_row(row_data)
            registration.google_sheet_row = row_number
            registration.save()
            
            print(f"[DEBUG] Data added to Google Sheets at row {row_number}")
        except Exception as sheet_error:
            sheets_error = str(sheet_error)
            print(f"[ERROR] Google Sheets error: {sheets_error}")
            print(traceback.format_exc())
        
        # Return success even if sheets failed
        response_data = {
            'success': True,
            'message': 'تم إرسال طلبك بنجاح!',
            'registration_id': registration.id
        }
        
        if sheets_error:
            response_data['warning'] = f'تم حفظ البيانات محلياً ولكن فشل الإرسال إلى Google Sheets: {sheets_error}'
        
        return JsonResponse(response_data)
        
    except Exception as e:
        error_msg = str(e)
        print(f"[ERROR] Unexpected error in submit_registration: {error_msg}")
        print(traceback.format_exc())
        return JsonResponse({
            'success': False,
            'error': f'خطأ غير متوقع: {error_msg}'
        }, status=500)
