from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView
# Create your views here.
from .models import *

def index(request):
    context = {
        'courses': Course.objects.all()
    }
    return render(request, 'index.html', context)

def course(request):
    context = {
        'courses': Course.objects.all()
    }
    return render(request, 'course.html', context)

# class HomeView(TemplateView):
#     template_name = "index.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['courses'] = Course.objects.all()[:2]
#         return context

    
