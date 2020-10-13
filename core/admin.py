from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Course)
admin.site.register(CourseItem)
admin.site.register(Teacher)
admin.site.register(Enroll)
admin.site.register(Heading)