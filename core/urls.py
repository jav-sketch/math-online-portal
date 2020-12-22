from django.urls import path
from .views import *
# from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView


app_name = 'core'
urlpatterns = [
    path('favicon.ico', RedirectView.as_view(
        url=staticfiles_storage.url('img/favicon.ico'))),
    path('', HomeView.as_view(), name='index'),
    path('course/', CourseView.as_view(), name="course"),
    path('course/<slug>/', CourseView.as_view(), name="course"),
    path('detail/<slug>/', CourseDetailView.as_view(), name="detail"),
    # path('enroll/<slug>/', EnrollDetailView.as_view(), name='enroll-summary'),
    path('enroll-summary/', EnrollSummaryView.as_view(), name='enroll-summary'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add-coupon/',
         AddCouponView.as_view(), name='add-coupon'),
    path('add-course/<slug>/', add_course, name='add-course'),
    path('remove-course/<slug>/', remove_course, name='remove-course'),
    path('payment/<payment>/', PaymentView.as_view(), name='payment'),
    path('refund-request/', RefundRequestView.as_view(), name='refund-request'),
    # path('remove-single-course/<slug>/',
    #      remove_single_course_item, name='remove-single-course'),
]
