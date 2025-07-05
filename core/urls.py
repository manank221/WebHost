from django.urls import path
from . import views
from .views import HomeView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('service/<slug:slug>/', views.service_detail, name='service_detail'),
    path('core/chat/', views.chat_assistant, name='chat_assistant'),
] 