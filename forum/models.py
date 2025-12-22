from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Theme(models.Model):


    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField()
    question = models.CharField()
    other_content = models.CharField(null=True)
    media = models.ImageField(null=True, blank=True, upload_to='theme_static/')



class Posts(models.Model):

    react_choices = [
        ('LIKE', 'LIKE'),
        ('DISLIKE', 'DISLIKE'),
        ('BEST', 'BEST')
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField()
    media = models.ImageField(null=True, blank=True, upload_to='posts_static/')
    reaction = models.CharField(max_length=20, choices=react_choices)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)

