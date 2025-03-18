from django.urls import path
from .views import show_info_page

urlpatterns = [
    path('', show_info_page, name='info_page'),
]