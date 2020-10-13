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
    ('SC', 'SATURDAY CLASSES'),
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
    specification = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Enroll(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    enrolled = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    enrolled_dated = models.DateTimeField()
    courses = models.ManyToManyField(CourseItem)

    def __str__(self):
        return self.user.username 


class Heading(models.Model):
    title = models.CharField(max_length=50, null=True)
    description = models.TextField()

    def __str__(self):
        return self.title
    
