from django.db import models
from urllib.parse import urlparse, parse_qs

# Create your models here.

class Material(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='materials/', blank=True, null=True)
    video = models.FileField(upload_to='materials/videos/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # парсить ID з YouTube-URL для embed
    def get_youtube_id(self):
        # Перевіряємо, чи тип контенту 'youtube' і чи є URL
        if self.url and 'youtube.com' in self.url or 'youtu.be' in self.url:
            # Розбираємо URL на компоненти (схема, хост, шлях, параметри тощо)
            parsed_url = urlparse(self.url)

            # Якщо це короткий URL (youtu.be), ID беремо з шляху (path) після першого слеша
            if parsed_url.hostname == 'youtu.be':
                return parsed_url.path[1:]
            
            # Якщо це стандартний YouTube-URL (youtube.com або www.youtube.com)
            if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
                # Для формату /watch?v=ID (наприклад, /watch?v=dQw4w9WgXcQ)
                if parsed_url.path == '/watch':
                    # Витягуємо параметр 'v' із query-рядка (наприклад, v=dQw4w9WgXcQ)
                    return parse_qs(parsed_url.query).get('v', [None])[0]
                
                # Для формату /embed/ID (наприклад, /embed/dQw4w9WgXcQ)
                if parsed_url.path[:7] == '/embed/':
                    return parsed_url.path.split('/')[2]
                
                # Для формату /v/ID (старий формат, наприклад, /v/dQw4w9WgXcQ)
                if parsed_url.path[:3] == '/v/':
                    return parsed_url.path.split('/')[2]
        return None

    def __str__(self):
        return self.name