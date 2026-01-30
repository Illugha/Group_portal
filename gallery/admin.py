from django.contrib import admin
from .models import Mediafiles

@admin.register(Mediafiles)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'author', 'status']
    list_filter = ['status', 'media_type']