from django.contrib import admin
from .models import Portfolio, Screenshot, Attachment, ExternalLink

class ScreenshotInline(admin.TabularInline):
    model = Screenshot
    extra = 0

class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0

class ExternalLinkInline(admin.TabularInline):
    model = ExternalLink
    extra = 0

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at')
    inlines = [ScreenshotInline, AttachmentInline, ExternalLinkInline]
