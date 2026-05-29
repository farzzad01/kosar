from django.urls import path
from .views import registration, submit_registration, login_view, google_login, google_callback

urlpatterns = [
    path('', registration, name='registration'),
    path('submit/', submit_registration, name='submit_registration'),
    path('login/', login_view, name='login'),
    path('auth/google/', google_login, name='google_login'),
    path('auth/google/callback/', google_callback, name='google_callback'),
]
