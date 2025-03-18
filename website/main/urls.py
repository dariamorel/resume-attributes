from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_home_page, name='home'),  # при переходе на главную страничку будет вызываться метод show_home_page
]