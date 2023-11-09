from django.contrib import admin

from . import models

# Register your models here.



@admin.register(models.Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = ['label']
    search_fields=['label']
