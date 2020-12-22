from django.contrib import admin
from .models import *

# class RefundAdmin(admin.ModelAdmin):


class EnrollAdmin(admin.ModelAdmin):
    list_display = ['user', 'enrolled',
                    'refund_requested', 'refund_granted',
                    'payment', 'billing_address', 'coupon']

    list_display_links = ['user', 'payment',
                          'billing_address',  'coupon']

    list_filter = ['enrolled', 'refund',
                   'refund_requested', 'refund_granted']

    search_fields = ['user__username',
                     'ref_code', ]


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
admin.site.register(Refund)
