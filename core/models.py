from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

# Create your models here.

# Course Model
CATEGORY = (
    ('FT', 'FULL TIME'),
    ('AS', 'AFTER SCHOOL'),
    ('EC', 'EVENING CLASSES'),
    ('PT', 'PRIVATE TUTORING'),
    ('S', 'SATURDAY CLASSES'),
    ('SC', 'SPECIALIZED COURSES'),
)

CATEGORY_CHOICES = (
    ('None', 'NONE'),
    ('Part-Time', 'PART-TIME'),
    ('Full-Time', 'FULL-TIME'),
)


class Course(models.Model):
    title = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY, max_length=20)
    evening = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    schedule = models.TextField(max_length=200)
    description = models.TextField()
    slug = models.SlugField()
    image = models.ImageField()
    def __str__(self):
        return self.title

    # Shortcut Method
    # Enrollment Link
    # def get_absolute_url(self):
    #     return reverse("core:enroll-summary", kwargs={
    #         'slug': self.slug
    #     })

    # Course Details
    def get_absolute_url_details(self):
        return reverse("core:detail", kwargs={
            'slug': self.slug
        })

    # Add course functionality
    def add_course_url(self):
        return reverse("core:add-course", kwargs={
            'slug': self.slug
        })

    # Remove course functionality
    def remove_course_url(self):
        return reverse("core:remove-course", kwargs={
            'slug': self.slug
        })

    def remove_single_course_item_url(self):
        return reverse("core:remove-single-course", kwargs={
            'slug': self.slug
        })

# CourseItem Model


class CourseItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    enrolled = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.course.title}"

    # Total Price Method
    def get_total_course_price(self):
        return self.quantity * self.course.price

    # Discount Price Method
    def get_total_discount_course_price(self):
        return self.quantity * self.course.discount_price

    # Saving Feature
    def get_amount_saved(self):
        return self.get_total_course_price() - self.get_total_discount_course_price()

    # Final Price method
    def final_price(self):
        if self.course.discount_price:
            return self.get_total_discount_course_price()
        return self.get_total_course_price()

# Teacher Model


class Teacher(models.Model):
    name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    specification = models.ForeignKey(
        Course, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

# Enroll Model
class Enroll(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    courses = models.ManyToManyField(CourseItem)
    enrolled = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    enrolled_date = models.DateTimeField()
    billing_address = models.ForeignKey(
        'BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username

    # Maximum Total
    def total(self):
        total = 0
        for course_item in self.courses.all():
            total += course_item.final_price()
        return total


class Heading(models.Model):
    title = models.CharField(max_length=50, null=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Section(models.Model):
    name = models.CharField(max_length=50, null=True)
    detail = models.TextField()

    def __str__(self):
        return self.name

# Billing Address


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    address = models.CharField(max_length=50, null=True)
    address_2 = models.CharField(max_length=50, null=True)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username  


#Discount method
class Coupon(models.Model):
    code = models.CharField(max_length=15)

    def __str__(self):
        return self.code