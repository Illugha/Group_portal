from django.contrib import admin
from .models import Subject, Grade

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "score", "date")
    list_filter = ("subject", "date")
    search_fields = ("student__full_name", "subject__name")




