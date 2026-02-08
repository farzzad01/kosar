from django.urls import path
from .views import home, get_occupied_slots

urlpatterns = [
    path('', home, name='home'),
    path('api/occupied-slots/', get_occupied_slots, name='occupied_slots'),
]
