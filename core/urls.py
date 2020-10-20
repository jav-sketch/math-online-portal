from django.urls import path
from .views import *
# from . import views



app_name = 'core'
urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('course/', CourseView.as_view(), name="course"),
    path('course/<slug>/', CourseView.as_view(), name="course"),
    # path('detail/<slug>/', CourseDetailView.as_view(), name="detail"),
    path('enroll/<slug>/', EnrollDetailView.as_view(), name='enroll-summary'),
    path('add-course/<slug>/', add_course, name='add-course'),
    path('remove-course/<slug>/', remove_course, name='remove-course'),
    path('remove-single-course/<slug>/', remove_single_course_item, name='remove-single-course'),
]
