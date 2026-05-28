from django.urls import path
from .views import home, registration, submit_registration

urlpatterns = [
    path('', home, name='home'),
    path('registration/', registration, name='registration'),
    path('submit/', submit_registration, name='submit_registration'),
]
