from django.contrib import admin
from .models import Programme, Level, Setting

# Register your models here.
admin.site.register(Setting)
admin.site.register(Programme)
admin.site.register(Level)