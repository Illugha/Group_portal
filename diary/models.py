from django.db import models
# from django.contrib.auth.models import User
from core.models import UserProfile

# class Student(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     full_name = models.CharField(max_length=150)

#     def __str__(self):
#         return self.full_name


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Grade(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades')
    score = models.IntegerField()
    date = models.DateField(auto_now_add = True)

    def __str__(self):
        return f"{self.student} — {self.subject}: {self.score}"



        
