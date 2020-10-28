from django.db import models
from django.conf import settings
from django.shortcuts import reverse

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


class Teacher(models.Model):
    name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    specification = models.ForeignKey(
        Course, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Enroll(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    courses = models.ManyToManyField(CourseItem)
    enrolled = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    enrolled_date = models.DateTimeField()

    def __str__(self):
        return self.user.username


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
