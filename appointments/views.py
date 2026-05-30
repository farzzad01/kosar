from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django_ratelimit.decorators import ratelimit
from .models import StudentRegistration
from .google_sheets_service import GoogleSheetsService
from datetime import datetime
import traceback
import requests
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests


def verify_recaptcha(token):
    """Verify reCAPTCHA token"""
    if not token:
        return False
    
    try:
        response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': settings.RECAPTCHA_PRIVATE_KEY,
                'response': token
            },
            timeout=5
        )
        result = response.json()
        return result.get('success', False)
    except Exception as e:
        print(f"[ERROR] reCAPTCHA verification failed: {str(e)}")
        return False


def registration(request):
    """Registration form page"""
    return render(request, 'registration.html', {
        'recaptcha_site_key': settings.RECAPTCHA_PUBLIC_KEY
    })


@ratelimit(key='ip', rate='5/h', method='POST')  # 5 submissions per hour per IP
@require_http_methods(["POST"])
def submit_registration(request):
    """Handle registration form submission - Stateless version for Vercel"""
    
    # Check rate limit
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        return JsonResponse({
            'success': False,
            'error': 'لقد تجاوزت الحد المسموح من المحاولات. يرجى المحاولة بعد ساعة.'
        }, status=429)
    
    try:
        # Verify reCAPTCHA
        recaptcha_response = request.POST.get('g-recaptcha-response')
        if not verify_recaptcha(recaptcha_response):
            return JsonResponse({
                'success': False,
                'error': 'فشل التحقق من reCAPTCHA. يرجى المحاولة مرة أخرى.'
            }, status=400)
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
            'personal_photo': 'صورة الشخص',
            'transcript': 'كشف درجات البكالوريوس'
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
            if not request.POST.get('master_university'):
                missing_fields.append('جامعة الماجستير')
            if not request.FILES.get('master_transcript'):
                missing_files.append('كشف درجات الماجستير')
            if not request.FILES.get('master_certificate'):
                missing_files.append('وثيقة الماجستير')
        
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
        master_university = request.POST.get('master_university', '')
        bachelor_gpa = request.POST.get('bachelor_gpa', '')
        master_gpa = request.POST.get('master_gpa', '')
        
        print(f"[DEBUG] Received data: {middle_name} {last_name}, {degree}, {phone}")
        
        # Get uploaded files
        passport = request.FILES.get('passport')
        personal_photo = request.FILES.get('personal_photo')
        transcript = request.FILES.get('transcript')
        master_transcript = request.FILES.get('master_transcript')
        master_certificate = request.FILES.get('master_certificate')
        
        # Prepare files dict for Drive upload
        files_dict = {
            'passport': passport,
            'personal_photo': personal_photo,
            'transcript': transcript,
            'master_transcript': master_transcript,
            'master_certificate': master_certificate
        }
        
        print(f"[DEBUG] Files received: {list(files_dict.keys())}")
        
        # Generate a unique registration ID (timestamp-based)
        registration_id = f"REG-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Send directly to Google Sheets (skip database)
        try:
            sheets_service = GoogleSheetsService()
            
            degree_display = 'ماجستير' if degree == 'master' else 'دكتوراه'
            full_name = f"{middle_name} {last_name}"
            
            # Prepare row data with placeholder for file links
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
                master_university if master_university else '',
                bachelor_gpa,
                master_gpa if master_gpa else '',
                passport.name if passport else '',
                personal_photo.name if personal_photo else '',
                transcript.name if transcript else '',
                master_transcript.name if master_transcript else '',
                master_certificate.name if master_certificate else '',
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ]
            
            # Add row with files (will upload to Drive and replace with links)
            row_number = sheets_service.add_row(row_data, files=files_dict)
            
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



def login_view(request):
    """Login page"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('admin:index')
        else:
            messages.error(request, 'البريد الإلكتروني أو كلمة المرور غير صحيحة')
    
    return render(request, 'login.html')


def google_login(request):
    """Redirect to Google OAuth"""
    from urllib.parse import urlencode
    
    client_id = settings.GOOGLE_OAUTH_CLIENT_ID
    redirect_uri = request.build_absolute_uri('/auth/google/callback/')
    
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': 'openid email profile',
        'access_type': 'online',
    }
    
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    return redirect(auth_url)


def google_callback(request):
    """Handle Google OAuth callback"""
    code = request.GET.get('code')
    
    if not code:
        messages.error(request, 'فشل تسجيل الدخول باستخدام Google')
        return redirect('login')
    
    try:
        # Exchange code for token
        token_url = 'https://oauth2.googleapis.com/token'
        client_id = settings.GOOGLE_OAUTH_CLIENT_ID
        client_secret = settings.GOOGLE_OAUTH_CLIENT_SECRET
        redirect_uri = request.build_absolute_uri('/auth/google/callback/')
        
        token_data = {
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        }
        
        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()
        
        if 'id_token' not in token_json:
            raise Exception('No ID token received')
        
        # Verify ID token
        idinfo = id_token.verify_oauth2_token(
            token_json['id_token'],
            google_requests.Request(),
            client_id
        )
        
        # Get user info
        email = idinfo.get('email')
        name = idinfo.get('name', '')
        
        # Authenticate or create user
        from django.contrib.auth.models import User
        user, created = User.objects.get_or_create(
            username=email,
            defaults={
                'email': email,
                'first_name': name,
            }
        )
        
        # Log the user in
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, f'مرحباً {name}!')
        return redirect(settings.LOGIN_REDIRECT_URL)
        
    except Exception as e:
        print(f"[ERROR] Google OAuth error: {str(e)}")
        messages.error(request, 'حدث خطأ أثناء تسجيل الدخول باستخدام Google')
        return redirect('login')
