from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.core.validators import MaxValueValidator, MinValueValidator
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
ADDRESS_CHOICES = (
    ('Billing', 'Billing'),
    ('Shipping', 'Shipping'),
)


class Course(models.Model):
    title = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY, max_length=20)
    evening = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    duration = models.DurationField(default=timedelta)
    subject = models.ForeignKey("Subject", on_delete=models.SET_NULL, null=True )
    schedule = models.TextField(max_length=200)
    description = models.TextField()
    slug = models.SlugField()
    image = models.ImageField(upload_to='course_pic')

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

 # CSEC Subjects
class Subject(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(default='subject.png',upload_to='subject_img')


    def __str__(self):
        return self.title


#User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, null=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField()
    is_staff = models.ForeignKey('StaffMember', on_delete=models.SET_NULL, null=True )
    is_superuser = models.BooleanField(default=False)
    image = models.ImageField(default='default.jpg', upload_to='profile_pic')


    def __str__(self):
        return f'{self.user.username} UserProfile'

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


# Assignment Model
class Assignment(models.Model):
    ASSIGNMENT_TYPE = (
        ('essay', "Essay"),

    )

    ASSIGNMENT_GRADE = (
        ('a+', 'A+'),
    )
    course = models.ForeignKey("Course", on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now=True)
    assignment_type = models.CharField(choices=ASSIGNMENT_TYPE, max_length=15, default='essay')
    due_date = models.DateTimeField()
    grade = models.CharField(choices=ASSIGNMENT_GRADE, max_length=3, default='a+')
    file = models.FileField(upload_to='assignment_files')
    progress = models.IntegerField()

    def __str__(self):
        return f"{self.pk}"
    


# Enroll Model
class Enroll(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)                         
    courses = models.ManyToManyField(CourseItem)
    enrolled = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    enrolled_date = models.DateTimeField()
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)   
    # progress = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)    
    refund_granted = models.BooleanField(default=False)    

    # Use case of the process to be outlined    
    ''' 
    1. User enrolled into a a Course
    2. Adding a Billing address(failed checkout)
    3. Payment 
    (Preprocessing, processing, etc.)
    4. Student can be enrolled in Courses
    5. Student can denroll from course
    6. Refunds
    '''    
    def __str__(self):
        return self.user.username

    # Maximum Total
    def total(self):
        total = 0
        for course_item in self.courses.all():
            total += course_item.final_price()
        if self.coupon:
            total -= self.coupon.amount    
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

#about model
class About(models.Model):
    title = models.CharField(max_length=50, null=True)
    description= models.TextField()
    owner = models.CharField(max_length=50, null=True)
    owner_description = models.TextField()
    owner_description_2 = models.TextField()
    owner_image = models.ImageField(default='default.png', upload_to='owner_img')

    def __str__(self):
        return self.title


# Learn more 
class LearnMore(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.title



# Staff
class StaffMember(models.Model):
    staff_member = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True)
    staff_member_description = models.TextField()
    staff_member_image = models.ImageField(default='default.png', upload_to='staff_member_img')

    def __str__(self):
        return str(self.staff_member)


# Address
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    address = models.CharField(max_length=50, null=True)
    address_2 = models.CharField(max_length=50, null=True)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=50)
    address_type = models.CharField(max_length=50, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'    



class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


# Discount method
class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    enroll = models.ForeignKey(Enroll, on_delete=models.CASCADE)
    reason = models.TextField()
    # ref_code = models.Charfield()
    accepted = models.BooleanField(default=False)
    email = models.EmailField(max_length=20)

    def __str__(self):
        return f"{self.pk}"

#Course Review Model
class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField(max_length=500)
    rating = models.FloatField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

# Top Featured Courses
# class FeaturedCourses(models.Model):
#     pass



# Django Signals function
def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
