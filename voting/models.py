from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone



class Vote(models.Model):
    """Модель голосування"""
    title = models.CharField(max_length=200, verbose_name="Назва голосування")
    description = models.TextField(verbose_name="Опис голосування")
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_votes',
        verbose_name="Створено користувачем"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    # Додаткові поля для розширеного функціоналу
    is_active = models.BooleanField(default=True, verbose_name="Активне")
    start_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата початку")
    end_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата завершення")  # ВИПРАВЛЕНО
    allow_revote = models.BooleanField(default=True, verbose_name="Дозволити переголосування")
    is_anonymous = models.BooleanField(default=False, verbose_name="Анонімне голосування")


    class Meta:
        verbose_name = "Голосування"
        verbose_name_plural = "Голосування"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def clean(self):
        """Валідація дат"""
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValidationError("Дата завершення має бути пізніше початку")
            
    def is_open(self):
        """Перевірка, чи відкрите голосування"""
        if not self.is_active:
            return False
        
        now = timezone.now()
        
        # Якщо є дата початку і вона ще не настала
        if self.start_date and now < self.start_date:
            return False
        
        # Якщо є дата завершення і вона вже минула
        if self.end_date and now > self.end_date:
            return False
        
        # Якщо немає дат або вони в допустимому діапазоні
        return True
    
    def total_votes(self):
        """Загальна кількість голосів"""
        return VoteResponse.objects.filter(vote_option__vote=self).values('user').distinct().count()
    
    def unique_voters(self):
        """Кількість унікальних користувачів, які проголосували"""
        return self.total_votes()  # По суті це те саме
    

class VoteOption(models.Model):
    """Модель варіанту відповіді для голосування"""
    vote = models.ForeignKey(
        Vote, 
        on_delete=models.CASCADE, 
        related_name='options',
        verbose_name="Голосування"
    )
    text = models.CharField(max_length=200, verbose_name="Текст варіанту")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок відображення")
    
    class Meta:
        verbose_name = "Варіант голосування"
        verbose_name_plural = "Варіанти голосування"
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.vote.title} - {self.text}"
    
    def vote_count(self):
        """Кількість голосів за цей варіант"""
        return self.responses.count()
    
    def vote_percentage(self):
        """Відсоток голосів від загальної кількості"""
        total = self.vote.total_votes()
        if total == 0:
            return 0
        return round((self.vote_count() / total) * 100, 1)


class VoteResponse(models.Model):
    """Модель відповіді користувача"""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='vote_responses',
        verbose_name="Користувач"
    )
    vote_option = models.ForeignKey(
        VoteOption, 
        on_delete=models.CASCADE, 
        related_name='responses',
        verbose_name="Обраний варіант"
    )
    voted_at = models.DateTimeField(auto_now_add=True, verbose_name="Час голосування")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Час оновлення")
    
    class Meta:
        verbose_name = "Відповідь користувача"
        verbose_name_plural = "Відповіді користувачів"
        # Якщо не дозволяється переголосування, можна додати unique_together
        # unique_together = ['user', 'vote_option__vote']
        ordering = ['-voted_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.vote_option.vote.title}"
    
    @classmethod
    def has_user_voted(cls, user, vote):
        """Перевірка, чи голосував користувач"""
        return cls.objects.filter(
            user=user, 
            vote_option__vote=vote
        ).exists()
    
    @classmethod
    def get_user_response(cls, user, vote):
        """Отримати відповідь користувача"""
        try:
            return cls.objects.get(user=user, vote_option__vote=vote)
        except cls.DoesNotExist:
            return None