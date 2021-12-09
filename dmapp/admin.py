from django.contrib import admin
from dmapp.models import CustomerInfo


@admin.register(CustomerInfo)
class CustomerInfoAdmin(admin.ModelAdmin):
    pass
