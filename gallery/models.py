from django.db import models
from django.contrib.auth.models import User

class Mediafiles(models.Model):
    MEDIA_TYPES = (
        ('photo', 'Фото'),
        ('gif', "GIF"),
        ('video', 'Видео'),
        ('audio', 'Аудио'),
    )

    STATUS = (
        ('pending', 'На модерации'),
        ('approved', 'Опубликовано'),
        ('rejected', 'Отклонено'),
    )

    title = models.CharField(max_length=200, verbose_name='Название')  
    description = models.TextField(blank=True, verbose_name='Описание')
    media_file = models.FileField(upload_to='gallery/', verbose_name='Файл')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default='photo', verbose_name='Тип')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    status = models.CharField(max_length=10, choices=STATUS, default='pending', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'медиафайл'
        verbose_name_plural = 'медиафайлы'

    def __str__(self):
        return f"{self.title} ({self.get_media_type_display()})"

    def save(self, *args, **kwargs):
        if self.media_file:
            ext = self.media_file.name.split('.')[-1]
            if ext =='gif':
                self.media_type = 'gif'
            if ext in ['jpg', 'jpeg', 'png']:
                self.media_type = 'photo'
            elif ext in ['mp4', 'avi']:
                self.media_type = 'video'
            elif ext in ['mp3']:
                self.media_type = 'audio'
        super().save(*args, **kwargs)