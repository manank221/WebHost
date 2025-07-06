from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import TemplateView
from .models import Service, Testimonial, About, SiteSettings
from portfolio.models import Project
from core.contact.forms import ContactForm
from core.contact.views import ContactView  # Re-use the email logic
import os
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse


class HomeView(ContactView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'services': Service.objects.all().order_by('order'),
            'testimonials': Testimonial.objects.all().order_by('order'),
            'about': About.objects.first(),
            'projects': Project.objects.filter(is_featured=True).order_by('order')[:6],
            'site_settings': SiteSettings.objects.first(),
        })
        # Add daily quote logic
        import datetime
        quotes_list = [
            ("The only way to do great work is to love what you do.", "Steve Jobs"),
            ("Success is not final, failure is not fatal: It is the courage to continue that counts.", "Winston Churchill"),
            ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
            ("The best way to get started is to quit talking and begin doing.", "Walt Disney"),
            ("Don't watch the clock; do what it does. Keep going.", "Sam Levenson"),
            ("Opportunities don't happen. You create them.", "Chris Grosser"),
            ("It does not matter how slowly you go as long as you do not stop.", "Confucius"),
            ("Everything you've ever wanted is on the other side of fear.", "George Addair"),
            ("Hardships often prepare ordinary people for an extraordinary destiny.", "C.S. Lewis"),
            ("Your time is limited, so don't waste it living someone else's life.", "Steve Jobs"),
        ]
        day_of_year = datetime.datetime.now().timetuple().tm_yday
        quote, author = quotes_list[day_of_year % len(quotes_list)]
        context['daily_quote'] = quote
        context['daily_author'] = author
        return context

    def post(self, request, *args, **kwargs):
        # This will reuse the same POST handling logic from ContactView
        response = super().post(request, *args, **kwargs)
        # Redirect back to the home page's contact section
        return redirect('core:home' + '#contact')


class AboutView(TemplateView):
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about'] = About.objects.filter(is_active=True).first()
        context['services'] = Service.objects.filter(is_active=True)
        context['site_settings'] = SiteSettings.objects.first()
        return context


class ServicesView(TemplateView):
    template_name = 'core/services.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.filter(is_active=True)
        context['site_settings'] = SiteSettings.objects.first()
        return context


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    return render(request, 'core/service_detail.html', {'service': service})


def about(request):
    about = About.objects.filter(is_active=True).first()
    services = Service.objects.filter(is_active=True)
    settings = SiteSettings.objects.first()
    
    context = {
        'about': about,
        'services': services,
        'site_settings': settings,
    }
    return render(request, 'core/about.html', context)


@csrf_exempt
def chat_assistant(request):
    if request.method == "POST":
        data = json.loads(request.body)
        question = data.get("question", "")
        
        # Get website context for better assistance
        site_settings = SiteSettings.objects.first()
        services = Service.objects.filter(is_active=True)
        service_list = ", ".join([service.title for service in services])
        
        # Create system prompt with website context
        system_prompt = f"""You are a helpful AI assistant for SkillGrid, a freelance services website. 

Website Information:
- Site Name: {site_settings.site_name if site_settings else 'SkillGrid'}
- Services Offered: {service_list}
- Contact Email: {site_settings.contact_email if site_settings else 'Not available'}

Your role:
1. Help users with questions about the website services
2. Provide information about web design, content writing, graphic design, logo design, translation, counselling, and notes services
3. Guide users to contact the owner for specific project inquiries
4. Engage in normal conversation when users want to chat
5. Be friendly, professional, and helpful
6. If you don't know something specific about the website, suggest they contact the owner

Always be helpful and conversational. If someone asks about pricing or specific project details, suggest they use the contact form or email the owner directly."""
        
        answer = None
        # Try Ollama first if it's enabled in settings
        if getattr(settings, 'OLLAMA_ENABLED', False):
            answer = try_ollama(question, system_prompt)
        
        # If Ollama is disabled or fails, try Hugging Face
        if not answer:
            answer = try_huggingface(question)
        
        # If both fail, provide a helpful fallback
        if not answer:
            answer = "I'm here to help! Feel free to ask me about our services. For specific project inquiries, please use our contact form or send an email."
            
        return JsonResponse({"answer": answer})
    
    return JsonResponse({"answer": "Please send a POST request with your question."})

def try_ollama(question, system_prompt):
    """Try to get response from local Ollama AI using settings."""
    try:
        url = f"{settings.OLLAMA_HOST}/api/generate"
        payload = {
            "model": settings.OLLAMA_MODEL,
            "prompt": f"{system_prompt}\n\nUser: {question}\nAssistant:",
            "stream": False,
        }
        
        response = requests.post(url, json=payload, timeout=settings.OLLAMA_TIMEOUT)
        response.raise_for_status()  # Will raise an HTTPError for bad responses (4xx or 5xx)
        
        result = response.json()
        return result.get("response", "").strip()

    except requests.exceptions.RequestException as e:
        print(f"Ollama connection error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred with Ollama: {e}")
        
    return None

def try_huggingface(question):
    """Try to get response from Hugging Face free tier"""
    try:
        # Use a smaller, faster model for free tier
        url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        headers = {"Authorization": f"Bearer {os.environ.get('HF_API_TOKEN', '')}"}
        payload = {"inputs": question}
        
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "").strip()
            elif isinstance(result, dict):
                return result.get("generated_text", "").strip()
    except Exception as e:
        print(f"Hugging Face error: {e}")
    return None

def services(request):
    services_list = Service.objects.filter(is_active=True)
    return render(request, 'core/services.html', {'services': services_list})

def home(request):
    return render(request, 'core/home.html')

def create_superuser_view(request):
    User = get_user_model()
    username = 'admin'
    email = 'admin@example.com'
    password = 'admin1234'
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        return HttpResponse('Superuser created! Username: admin, Password: admin1234')
    else:
        return HttpResponse('Superuser already exists.') 