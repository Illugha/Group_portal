from django.test import TestCase
from django.contrib.auth.models import User
from .models import Student, Subject, Grade
import datetime

class ModelsTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="testuser")
        student = Student.objects.create(user=user, full_name="Test Student")
        subject = Subject.objects.create(name="Math")
        Grade.objects.create(student=student, subject=subject, score=10, date=datetime.date.today())

    def test_grade_created(self):
        grade = Grade.objects.first()
        self.assertEqual(grade.score, 10)



