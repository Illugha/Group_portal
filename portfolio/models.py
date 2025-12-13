from django.db import models
from django.conf import settings

class Portfolio(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='portfolios')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Screenshot(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='screenshots')
    image = models.ImageField(upload_to='portfolio/screenshots/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Screenshot {self.pk} for {self.portfolio_id}"

class Attachment(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='portfolio/files/')
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name or f"File {self.pk}"

class ExternalLink(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='links')
    name = models.CharField(max_length=200, blank=True)
    url = models.URLField()

    def __str__(self):
        return self.url
