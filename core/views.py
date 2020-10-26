from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView, ListView, View
from django.contrib import messages
from django.utils import timezone
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


# Enrollment
class EnrollDetailView(DetailView):
    model = Course
    template_name = "enroll.html"

    

#Checkout
def checkout(request):
    context = {}
    return render(request, "checkout.html", context)    



# Add course feature
@login_required
def add_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    course_item, created = CourseItem.objects.get_or_create(
        course=course,
        user=request.user,
        enrolled=False
    )
    enroll_qs = Enroll.objects.filter(user=request.user, enrolled=False)

    if enroll_qs.exists():
        enroll = enroll_qs[0]
        # This checks to see if a course item is in course
        if enroll.courses.filter(course__slug=course.slug).exists():
            """Adding Course to a Course Item."""
            course_item.quantity += 1
            course_item.save()
            messages.info(request, "Course quantity has been updated.")
            return redirect("core:course")
        else:
            enroll.courses.add(course_item)
            messages.info(request, "Course was added to your profile.")
            return redirect("core:enroll-summary", slug=slug)
    else:
        enrolled_date = timezone.now()        
        enroll = Enroll.objects.create(
            user=request.user, enrolled_date=enrolled_date)
        enroll.courses.add(course_item)
        messages.info(request, "You have added course to your profile.")  
        return redirect("core:enroll-summary", slug=slug)

#Removes or Deletes a Course
@login_required
def remove_course(request, slug):
    course =  get_object_or_404(Course, slug=slug)
    enroll_qs = Enroll.objects.filter(user=request.user, enrolled=False)
    # checks to see if a course object exist 
    if enroll_qs.exists():
        enroll = enroll_qs[0]
        if enroll.courses.filter(course__slug=course.slug).exists():
            course_item = CourseItem.objects.filter(
                course=course,
                user=request.user,
                enrolled=False
            )[0]
            #removes or deletes a course object if it exists
            enroll.courses.remove(course_item)
            messages.info(request, "You were successfully denrolled from the  course.")
            return redirect("core:enroll-summary", slug=slug)
        else:
            # If not redirects to course page.
            messages.info(request, "Sorry, you are not in a course. Please add a course to continue")
            return redirect("core:enroll-summary", slug=slug)
    else:
        messages.info(request, "Not enrolled in a course.")
        return redirect("core:enroll-summary", slug=slug)


@login_required
#Removing a single course quantity
def remove_single_course_item(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enroll_qs = Enroll.objects.filter(user=request.user, enrolled=False)
    # checks to see if a course object exist 
    if enroll_qs.exists():
        enroll = enroll_qs[0]
        if enroll.courses.filter(course__slug=course.slug).exists():
            course_item = CourseItem.objects.filter(
                course=course,
                user=request.user,
                enrolled=False
            )[0]
            #removes or deletes a course object if it exists
            """Removing Quantity from a Course Item"""
            course_item.quantity -= 1
            course_item.save()
            messages.info(request, "You were successfully denrolled from the  course.")
            return redirect("core:enroll-summary")
        else:
            messages.info(request, "Course was not found!")
            return redirect("core:enroll-summary", slug=slug)
    else:
        messages.info(request, "You are currently not enrolled in a course!")
        return redirect("core:enroll-summary", slug=slug)            


