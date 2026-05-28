from django.urls import path
from .views import registration, submit_registration

urlpatterns = [
    path('', registration, name='registration'),
    path('submit/', submit_registration, name='submit_registration'),
]
