from django.contrib import admin
from .models import Plan, Investment, Percentage

# Register your models here.
admin.site.register(Plan)
admin.site.register(Investment)
admin.site.register(Percentage)