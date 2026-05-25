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
    """Handle registration form submission - Stateless version for Vercel"""
    try:
        # Validate required fields
        required_fields = {
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
        first_name = ''  # Removed field
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
        
        print(f"[DEBUG] Received data: {middle_name} {last_name}, {degree}, {phone}")
        
        # Get uploaded files
        passport = request.FILES.get('passport')
        transcript = request.FILES.get('transcript')
        master_transcript = request.FILES.get('master_transcript')
        university_form = request.FILES.get('university_form')
        
        # Create file info
        file_info = {
            'passport': passport.name if passport else '',
            'transcript': transcript.name if transcript else '',
            'master_transcript': master_transcript.name if master_transcript else '',
            'university_form': university_form.name if university_form else ''
        }
        
        print(f"[DEBUG] Files received: {list(file_info.keys())}")
        
        # Generate a unique registration ID (timestamp-based)
        registration_id = f"REG-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Send directly to Google Sheets (skip database)
        try:
            sheets_service = GoogleSheetsService()
            
            degree_display = 'ماجستير' if degree == 'master' else 'دكتوراه'
            full_name = f"{middle_name} {last_name}"
            row_data = [
                registration_id,
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
                file_info.get('passport', ''),
                file_info.get('transcript', ''),
                file_info.get('master_transcript', ''),
                file_info.get('university_form', ''),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ]
            
            row_number = sheets_service.add_row(row_data)
            
            print(f"[DEBUG] Data added to Google Sheets at row {row_number}")
            
            return JsonResponse({
                'success': True,
                'message': 'تم إرسال طلبك بنجاح!',
                'registration_id': registration_id
            })
            
        except Exception as sheet_error:
            error_msg = str(sheet_error)
            print(f"[ERROR] Google Sheets error: {error_msg}")
            print(traceback.format_exc())
            return JsonResponse({
                'success': False,
                'error': f'خطأ في إرسال البيانات إلى Google Sheets: {error_msg}'
            }, status=500)
        
    except Exception as e:
        error_msg = str(e)
        print(f"[ERROR] Unexpected error in submit_registration: {error_msg}")
        print(traceback.format_exc())
        return JsonResponse({
            'success': False,
            'error': f'خطأ غير متوقع: {error_msg}'
        }, status=500)
