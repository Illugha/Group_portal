from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='static/media/', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="announcements", null=True, blank=True)
    def __str__(self):
        return self.title