from django.contrib import admin

# Register your models here.

from .models import BoardGame

admin.site.register(BoardGame)
