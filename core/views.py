from django.conf import settings
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
from .forms import *
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

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


# Enroll Summary
class EnrollSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            enroll = Enroll.objects.get(user=self.request.user, enrolled=False)
            context = {
                'object': enroll
            }
            return render(self.request, 'enroll.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "Not Enrolled in a Course!")
            return redirect("core:course")


# Description of  Courses
class CourseDetailView(DetailView):
    model = Course
    template_name = "details.html"


# Enrollment
class EnrollDetailView(DetailView):
    model = Course
    template_name = "enroll.html"


# Checkout
class CheckoutView(View):
    def get(self, *args, **kwargs):
        # Forms
        form = CheckoutForm()
        context = {
            'form': form,
        }
        return render(self.request, "checkout.html", context)
    # Post Method

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        print(self.request.POST)
        try:
            enroll = Enroll.objects.get(user=self.request.user, enrolled=False)
            if form.is_valid():
                print(form.cleaned_data)
                print("Form is valid")
                address = form.cleaned_data.get('address')
                address_2 = form.cleaned_data.get('address_2')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')
                save_info = form.cleaned_data.get('save_info')
                payment = form.cleaned_data.get('payment')
                billing_address = BillingAddress(
                    user=self.request.user,
                    address=address,
                    address_2=address_2,
                    country=country,
                    zip=zip,
                )
                billing_address.save()
                enroll.billing_address = billing_address
                enroll.save()
                if payment == 'Stripe':
                    return redirect('core:payment', payment='Stripe')
                elif payment == 'Paypal':
                    return redirect('core:payment', payment='Paypal')
                elif payment == 'MMG':
                    return redirect('core:payment', payment='MMG')
                else:
                    messages.warning(self.request,
                    "Invalid payment selection, please try again!")
                    return redirect("core:checkout")
            payment = form.cleaned_data.get('payment')        
            if payment == 'Stripe':
                    return redirect('core:payment', payment='Stripe')
            elif payment == 'Paypal':
                    return redirect('core:payment', payment='Paypal')        
            elif payment == 'MMG':
                    return redirect('core:payment', payment='MMG')    
            else:
                messages.warning(self.request,
                    "Invalid payment selection, please try again!")
                return redirect("core:checkout")                
        except ObjectDoesNotExist:
            messages.warning(self.request, "You are not in any course!")
            return redirect("core:enroll-summary")   

# Payment
class PaymentView(View):
    def get(self, *args, **kwargs):
        # Enroll
        enroll = Enroll.objects.get(user=self.request.user, enrolled=False)
        context = {
            'enroll': enroll 
        }
        return render(self.request, "payment.html", context)

    def post(self, *args, **kwargs):
        enroll = Enroll.objects.get(user=self.request.user, enrolled=False)
        token = self.request.POST.get('stripeToken')
        amount = int(enroll.total() * 100)
        try:
            # Creates the charge
            charge = stripe.Charge.create(
                amount=amount,
                currency="gyd",
                source=token,
                description="Charge for javonbrowne@gmail.com"
            )
            # Create the payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = enroll.total()
            payment.save()

            # Assign payment to enroll
            enroll.enrolled = True
            enroll.payment = payment
            enroll.save()
            messages.success(
                self.request, "payment was successfully processed.")
            return redirect("core:index")
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            messages.error(
                self.request, f"{e.user_message}")
            # print('Status is: %s' % e.http_status)
            # print('Code is: %s' % e.code)
            # # param is '' in this case
            # print('Param is: %s' % e.param)
            # print('Message is: %s' % e.user_message)
            return redirect("core:index")
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(
                self.request, "Rate Limit Error.")
            return redirect("core:index")
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(
                self.request, "Invalid parameters.")
            return redirect("core:index")
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(
                self.request, "Not Authenticated")
            return redirect("core:index")
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(
                self.request, "Network Error")
            return redirect("core:index")
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(
                self.request, "Something went wrong, you were not charged. Please try again.")
            return redirect("core:index")
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            messages.error(
                self.request, "A serious error occurred. We have been notified.")
            return redirect("core:index")


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
            return redirect("core:enroll-summary")
        else:
            enroll.courses.add(course_item)
            messages.info(request, "Course was added to your profile.")
            return redirect("core:enroll-summary")
    else:
        enrolled_date = timezone.now()
        enroll = Enroll.objects.create(
            user=request.user, enrolled_date=enrolled_date)
        enroll.courses.add(course_item)
        messages.info(request, "You have added course to your profile.")
        return redirect("core:course", slug=slug)

# Removes or Deletes a Course
@login_required
def remove_course(request, slug):
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
            # removes or deletes a course object if it exists
            enroll.courses.remove(course_item)
            messages.info(
                request, "You were successfully denrolled from the  course.")
            return redirect("core:enroll-summary",)
        else:
            # If not redirects to course page.
            messages.info(
                request, "Sorry, you are not in a course. Please add a course to continue")
            return redirect("core:course", slug=slug)
    else:
        messages.info(request, "Not enrolled in a course.")
        return redirect("core:enroll-summary", slug=slug)


@login_required
# Removing a single course quantity
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
            # removes or deletes a course object if it exists
            """Removing Quantity from a Course Item"""
            if course_item.quantity > 1:
                course_item.quantity -= 1
                course_item.save()
            else:
                enroll.courses.remove(course_item)
            messages.info(
                request, "You were successfully denrolled from the  course.")
            return redirect("core:enroll-summary")
        else:
            messages.info(request, "Course was not found!")
            return redirect("core:enroll-summary", slug=slug)
    else:
        messages.info(request, "You are currently not enrolled in a course!")
        return redirect("core:enroll-summary", slug=slug)
