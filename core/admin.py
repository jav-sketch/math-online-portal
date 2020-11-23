from django.contrib import admin
from .models import *
class EnrollAdmin(admin.ModelAdmin):
    list_display = ['user', 'enrolled']
    
# Register your models here.
admin.site.register(Course)
admin.site.register(CourseItem)
admin.site.register(Teacher)
admin.site.register(Enroll, EnrollAdmin)
admin.site.register(Heading)
admin.site.register(Section)
admin.site.register(BillingAddress)
admin.site.register(Payment)
admin.site.register(Coupon)