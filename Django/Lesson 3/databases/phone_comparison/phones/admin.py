from django.contrib import admin

# Register your models here.
from phones.models import Iphone, Samsung, Phone


class PhoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'devicetype', 'os', 'ram', 'price', 'cam', 'weight', 'display')


class IphoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'faceid', 'applepay')


class SamsungAdmin(admin.ModelAdmin):
    list_display = ('name', 'fm', 'samsungpay', 'ikport')


admin.site.register(Phone, PhoneAdmin)
admin.site.register(Iphone, IphoneAdmin)
admin.site.register(Samsung, SamsungAdmin)
