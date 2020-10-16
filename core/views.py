from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView, ListView
# Create your views here.
from .models import *


# Index Page
class HomeView(ListView):
    model = Heading
    template_name = "index.html"


# Courses template
class CourseView(ListView):
    model = Course
    template_name = "course.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['courses'] = Course.objects.all()[:]
    #     return context

# Description of  Courses   
class CourseDetailView(DetailView):
    model = Course
    template_name = "details.html"

#Enrollment
class EnrollDetailView(DetailView):
    model = Course
    template_name = "enroll.html"

# Enroll in course feature
def add_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    course_item = CourseItem.objects.get_or_create(
        course=course,
        user=request.user,
        enrolled=False
    )
    enroll_qs = Enroll.objects.filter(user=request.User, enrolled=False)

    if enroll_qs.exists():
        enroll = enroll_qs[0]
        # This checks to see if a course item is in course
        if enroll.courses.filter(course__slug=course.slug).exists():
            """Adding Course to a Course Item."""
            course_item.quantity += 1
            course_item.save()
        else:
            enroll.courses.add(course_item)
            return redirect("core:enroll", slug=slug)    
