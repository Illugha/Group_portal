from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Vote, VoteOption, VoteResponse
from .forms import VoteForm, VoteOptionFormSet, VoteResponseForm


class VoteModelTest(TestCase):
    """Тести для моделі Vote"""
    
    def setUp(self):
        """Підготовка тестових даних"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.vote = Vote.objects.create(
            title='Тестове голосування',
            description='Опис тестового голосування',
            created_by=self.user,
            is_active=True
        )
        
        self.option1 = VoteOption.objects.create(
            vote=self.vote,
            text='Варіант 1',
            order=1
        )
        
        self.option2 = VoteOption.objects.create(
            vote=self.vote,
            text='Варіант 2',
            order=2
        )
    
    def test_vote_creation(self):
        """Тест створення голосування"""
        self.assertEqual(self.vote.title, 'Тестове голосування')
        self.assertEqual(self.vote.created_by, self.user)
        self.assertTrue(self.vote.is_active)
    
    def test_vote_str(self):
        """Тест строкового представлення"""
        self.assertEqual(str(self.vote), 'Тестове голосування')
    
    def test_vote_is_open(self):
        """Тест перевірки відкритості голосування"""
        # Активне голосування без дат
        self.assertTrue(self.vote.is_open())
        
        # Неактивне голосування
        self.vote.is_active = False
        self.vote.save()
        self.assertFalse(self.vote.is_open())
        
        # Голосування ще не почалося
        self.vote.is_active = True
        self.vote.start_date = timezone.now() + timedelta(days=1)
        self.vote.save()
        self.assertFalse(self.vote.is_open())
        
        # Голосування завершилось
        self.vote.start_date = timezone.now() - timedelta(days=2)
        self.vote.end_date = timezone.now() - timedelta(days=1)
        self.vote.save()
        self.assertFalse(self.vote.is_open())
    
    def test_vote_total_votes(self):
        """Тест підрахунку загальної кількості голосів"""
        self.assertEqual(self.vote.total_votes(), 0)
        
        # Додаємо голоси
        VoteResponse.objects.create(user=self.user, vote_option=self.option1)
        self.assertEqual(self.vote.total_votes(), 1)
    
    def test_vote_unique_voters(self):
        """Тест підрахунку унікальних користувачів"""
        user2 = User.objects.create_user(username='user2', password='pass123')
        
        VoteResponse.objects.create(user=self.user, vote_option=self.option1)
        VoteResponse.objects.create(user=user2, vote_option=self.option2)
        
        self.assertEqual(self.vote.unique_voters(), 2)


class VoteOptionModelTest(TestCase):
    """Тести для моделі VoteOption"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.vote = Vote.objects.create(
            title='Тест',
            description='Опис',
            created_by=self.user
        )
        
        self.option = VoteOption.objects.create(
            vote=self.vote,
            text='Варіант A',
            order=1
        )
    
    def test_option_creation(self):
        """Тест створення варіанту"""
        self.assertEqual(self.option.text, 'Варіант A')
        self.assertEqual(self.option.vote, self.vote)
    
    def test_option_str(self):
        """Тест строкового представлення"""
        expected = f"{self.vote.title} - {self.option.text}"
        self.assertEqual(str(self.option), expected)
    
    def test_vote_count(self):
        """Тест підрахунку голосів за варіант"""
        self.assertEqual(self.option.vote_count(), 0)
        
        VoteResponse.objects.create(user=self.user, vote_option=self.option)
        self.assertEqual(self.option.vote_count(), 1)
    
    def test_vote_percentage(self):
        """Тест підрахунку відсотків"""
        option2 = VoteOption.objects.create(
            vote=self.vote,
            text='Варіант B',
            order=2
        )
        
        user2 = User.objects.create_user(username='user2', password='pass')
        
        VoteResponse.objects.create(user=self.user, vote_option=self.option)
        VoteResponse.objects.create(user=user2, vote_option=option2)
        
        self.assertEqual(self.option.vote_percentage(), 50.0)


class VoteResponseModelTest(TestCase):
    """Тести для моделі VoteResponse"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.vote = Vote.objects.create(
            title='Тест',
            description='Опис',
            created_by=self.user
        )
        
        self.option = VoteOption.objects.create(
            vote=self.vote,
            text='Варіант',
            order=1
        )
    
    def test_response_creation(self):
        """Тест створення відповіді"""
        response = VoteResponse.objects.create(
            user=self.user,
            vote_option=self.option
        )
        
        self.assertEqual(response.user, self.user)
        self.assertEqual(response.vote_option, self.option)
    
    def test_has_user_voted(self):
        """Тест перевірки чи голосував користувач"""
        self.assertFalse(VoteResponse.has_user_voted(self.user, self.vote))
        
        VoteResponse.objects.create(user=self.user, vote_option=self.option)
        self.assertTrue(VoteResponse.has_user_voted(self.user, self.vote))
    
    def test_get_user_response(self):
        """Тест отримання відповіді користувача"""
        self.assertIsNone(VoteResponse.get_user_response(self.user, self.vote))
        
        response = VoteResponse.objects.create(
            user=self.user,
            vote_option=self.option
        )
        
        user_response = VoteResponse.get_user_response(self.user, self.vote)
        self.assertEqual(user_response, response)


class VoteViewsTest(TestCase):
    """Тести для views"""
    
    def setUp(self):
        """Підготовка даних для тестування views"""
        self.client = Client()
        
        # Створення користувачів
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.moderator = User.objects.create_user(
            username='moderator',
            password='modpass123'
        )
        
        self.admin = User.objects.create_user(
            username='admin',
            password='adminpass123',
            is_staff=True
        )
        
        # Створення групи модераторів
        moderators_group = Group.objects.create(name='Moderators')
        self.moderator.groups.add(moderators_group)
        
        # Створення голосування
        self.vote = Vote.objects.create(
            title='Тестове голосування',
            description='Опис',
            created_by=self.admin,
            is_active=True
        )
        
        self.option1 = VoteOption.objects.create(
            vote=self.vote,
            text='Опція 1',
            order=1
        )
        
        self.option2 = VoteOption.objects.create(
            vote=self.vote,
            text='Опція 2',
            order=2
        )
    
    def test_vote_list_view(self):
        """Тест списку голосувань"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('voting:vote_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестове голосування')
        self.assertTemplateUsed(response, 'voting/vote_list.html')
    
    def test_vote_list_view_requires_login(self):
        """Тест що список потребує авторизації"""
        response = self.client.get(reverse('voting:vote_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_vote_detail_view(self):
        """Тест детального перегляду"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('voting:vote_detail', kwargs={'pk': self.vote.pk})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестове голосування')
        self.assertTemplateUsed(response, 'voting/vote_detail.html')
    
    def test_vote_results_view(self):
        """Тест перегляду результатів"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('voting:vote_results', kwargs={'pk': self.vote.pk})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'voting/vote_results.html')
    
    def test_vote_create_view_moderator(self):
        """Тест створення голосування модератором"""
        self.client.login(username='moderator', password='modpass123')
        response = self.client.get(reverse('voting:vote_create'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'voting/vote_form.html')
    
    def test_vote_create_view_regular_user(self):
        """Тест що звичайний користувач не може створювати"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('voting:vote_create'))
        
        self.assertEqual(response.status_code, 403)  # Forbidden
    
    def test_vote_update_view_admin(self):
        """Тест редагування голосування адміністратором"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(
            reverse('voting:vote_update', kwargs={'pk': self.vote.pk})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'voting/vote_form.html')
    
    def test_voting_process(self):
        """Тест процесу голосування"""
        self.client.login(username='testuser', password='testpass123')
        
        # Користувач ще не голосував
        self.assertFalse(
            VoteResponse.has_user_voted(self.user, self.vote)
        )
        
        # Голосування
        response = self.client.post(
            reverse('voting:vote_detail', kwargs={'pk': self.vote.pk}),
            {'vote_option': self.option1.pk}
        )
        
        # Перевірка редіректу
        self.assertEqual(response.status_code, 302)
        
        # Перевірка що голос збережено
        self.assertTrue(
            VoteResponse.has_user_voted(self.user, self.vote)
        )
        
        user_response = VoteResponse.get_user_response(self.user, self.vote)
        self.assertEqual(user_response.vote_option, self.option1)
    
    def test_revoting(self):
        """Тест переголосування"""
        self.vote.allow_revote = True
        self.vote.save()
        
        self.client.login(username='testuser', password='testpass123')
        
        # Перший голос
        self.client.post(
            reverse('voting:vote_detail', kwargs={'pk': self.vote.pk}),
            {'vote_option': self.option1.pk}
        )
        
        # Переголосування
        self.client.post(
            reverse('voting:vote_detail', kwargs={'pk': self.vote.pk}),
            {'vote_option': self.option2.pk}
        )
        
        # Перевірка що голос змінився
        user_response = VoteResponse.get_user_response(self.user, self.vote)
        self.assertEqual(user_response.vote_option, self.option2)
        
        # Перевірка що існує лише одна відповідь
        responses_count = VoteResponse.objects.filter(
            user=self.user,
            vote_option__vote=self.vote
        ).count()
        self.assertEqual(responses_count, 1)


class VoteFormsTest(TestCase):
    """Тести для форм"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.vote = Vote.objects.create(
            title='Тест',
            description='Опис',
            created_by=self.user
        )
    
    def test_vote_form_valid(self):
        """Тест валідної форми голосування"""
        form_data = {
            'title': 'Нове голосування',
            'description': 'Опис голосування',
            'is_active': True,
            'allow_revote': True,
            'is_anonymous': False
        }
        
        form = VoteForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_vote_form_invalid_dates(self):
        """Тест невалідних дат"""
        form_data = {
            'title': 'Тест',
            'description': 'Опис',
            'start_date': timezone.now() + timedelta(days=2),
            'end_date': timezone.now() + timedelta(days=1),
            'is_active': True
        }
        
        form = VoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Дата завершення має бути пізніше', str(form.errors))
    
    def test_vote_response_form(self):
        """Тест форми відповіді користувача"""
        option = VoteOption.objects.create(
            vote=self.vote,
            text='Варіант',
            order=1
        )
        
        form = VoteResponseForm(
            data={'vote_option': option.pk},
            vote=self.vote
        )
        
        self.assertTrue(form.is_valid())


class VoteIntegrationTest(TestCase):
    """Інтеграційні тести"""
    
    def setUp(self):
        self.client = Client()
        
        self.admin = User.objects.create_user(
            username='admin',
            password='adminpass123',
            is_staff=True
        )
        
        self.user1 = User.objects.create_user(
            username='user1',
            password='pass123'
        )
        
        self.user2 = User.objects.create_user(
            username='user2',
            password='pass123'
        )
    
    def test_full_voting_workflow(self):
        """Тест повного робочого процесу голосування"""
        
        # 1. Адмін входить в систему
        self.client.login(username='admin', password='adminpass123')
        
        # 2. Адмін створює голосування
        vote = Vote.objects.create(
            title='Улюблений колір',
            description='Оберіть ваш улюблений колір',
            created_by=self.admin,
            is_active=True,
            allow_revote=False
        )
        
        # 3. Додаємо варіанти
        red = VoteOption.objects.create(vote=vote, text='Червоний', order=1)
        blue = VoteOption.objects.create(vote=vote, text='Синій', order=2)
        green = VoteOption.objects.create(vote=vote, text='Зелений', order=3)
        
        # 4. Користувач 1 голосує
        self.client.login(username='user1', password='pass123')
        self.client.post(
            reverse('voting:vote_detail', kwargs={'pk': vote.pk}),
            {'vote_option': red.pk}
        )
        
        # 5. Користувач 2 голосує
        self.client.login(username='user2', password='pass123')
        self.client.post(
            reverse('voting:vote_detail', kwargs={'pk': vote.pk}),
            {'vote_option': blue.pk}
        )
        
        # 6. Перевірка результатів
        self.assertEqual(vote.total_votes(), 2)
        self.assertEqual(vote.unique_voters(), 2)
        self.assertEqual(red.vote_count(), 1)
        self.assertEqual(blue.vote_count(), 1)
        self.assertEqual(green.vote_count(), 0)
        
        # 7. Перевірка відсотків
        self.assertEqual(red.vote_percentage(), 50.0)
        self.assertEqual(blue.vote_percentage(), 50.0)
        self.assertEqual(green.vote_percentage(), 0.0)
        
        # 8. Користувач 1 намагається переголосувати (має бути заборонено)
        self.client.login(username='user1', password='pass123')
        response = self.client.post(
            reverse('voting:vote_detail', kwargs={'pk': vote.pk}),
            {'vote_option': blue.pk}
        )
        
        # Голос не повинен змінитися
        user1_response = VoteResponse.get_user_response(self.user1, vote)
        self.assertEqual(user1_response.vote_option, red)
