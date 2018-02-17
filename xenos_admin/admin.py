from django.contrib import admin
from .models import Plan, Investment, Percentage, Transaction, test_model, Post

# Register your models here.
admin.site.register(Plan)
admin.site.register(Investment)
admin.site.register(Percentage)
admin.site.register(Transaction)
admin.site.register(test_model)
admin.site.register(Post)