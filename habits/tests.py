from datetime import timedelta
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from habits.models import Habits
from user_auth.models import User

# Create your tests here.
TEST_CHAT_ID_ADMIN = 101
TEST_CHAT_ID_USER = 110
TEST_CHAT_ID_USER2 = 111
TEST_CHAT_ID_STAFF = 121

TEST_ADMIN_PASSWORD = '123abc123'
TEST_USER_PASSWORD = '124abc124'
TEST_USER_PASSWORD2 = '124abc124'
TEST_STAFF_PASSWORD = '125abc125'


class TestUser():
    """
    создание пользователей для тестирования
    """

    @staticmethod
    def create_user(*args, **kwargs):
        user = User.objects.create(
            chat_id=TEST_CHAT_ID_USER,
            first_name='Test',
            last_name='Just User',
            is_active=True,
            is_staff=False,
            is_superuser=False
        )
        user.set_password(TEST_USER_PASSWORD)
        user.save()
        return user

    @staticmethod
    def create_user2(*args, **kwargs):
        user = User.objects.create(
            chat_id=TEST_CHAT_ID_USER2,
            first_name='Test2',
            last_name='Just User2',
            is_active=True,
            is_staff=False,
            is_superuser=False
        )
        user.set_password(TEST_USER_PASSWORD2)
        user.save()
        return user


    @staticmethod
    def create_staff(*args, **kwargs):
        user = User.objects.create(
            chat_id=TEST_CHAT_ID_STAFF,
            first_name='Test',
            last_name='Staff',
            is_active=True,
            is_staff=True,
            is_superuser=False
        )
        user.set_password(TEST_STAFF_PASSWORD)
        user.save()
        return user

    @staticmethod
    def create_admin(*args, **kwargs):
        user = User.objects.create(
            chat_id=TEST_CHAT_ID_ADMIN,
            first_name='Test',
            last_name='Admin',
            is_active=True,
            is_staff=True,
            is_superuser=True
        )
        user.set_password(TEST_ADMIN_PASSWORD)
        user.save()
        return user


class TestHabits(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = TestUser.create_user()
        data = {"chat_id": self.user.chat_id,
                "password": TEST_USER_PASSWORD
                }
        # self.client.force_authenticate(self.user)
        self.url_token = reverse('token_obtain_pair')
        response = self.client.post(self.url_token, data)
        self.access_token = response.json().get('access')
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.habit = Habits.objects.create(
            user=self.user,
            place="театре",
            time="19:00:00",
            activity="смотреть спектакль",
            period="weekly",
            time_for_action=timedelta(seconds=40),
            is_public=True
        )
        self.habit.save()

    def test_habit_create_pleasant(self):
        number = Habits.objects.all().count()
        url = reverse('habits_create')
        data = {
            'place': "тестовое место",
            'time': "19:00:00",
            'activity': "тестовая привычка",
            'period': "weekly",
            'time_for_action': 40,
            'is_pleasant': True,
            'is_public': True}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habits.objects.count(), number + 1)
        habit = Habits.objects.order_by('id').last()
        self.assertEqual(habit.place, data['place'])
        self.assertEqual(habit.time.strftime('%H:%M:%S'), data['time'])
        self.assertEqual(habit.activity, data['activity'])
        self.assertEqual(habit.period, data['period'])
        self.assertEqual(habit.time_for_action, timedelta(
            seconds=data['time_for_action']))
        self.assertEqual(habit.is_public, data['is_public'])
        self.assertEqual(habit.is_pleasant, data['is_pleasant'])

    def test_habit_create_not_pleasant(self):
        number = Habits.objects.all().count()
        url = reverse('habits_create')
        data = {
            'place': "тестовое место",
            'time': "19:00:00",
            'activity': "тестовая привычка",
            'period': "weekly",
            'time_for_action': 40,
            'is_pleasant': False,
            'compensation': 'test compensation',
            'is_public': True}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habits.objects.count(), number + 1)
        habit = Habits.objects.order_by('id').last()
        self.assertEqual(habit.place, data['place'])
        self.assertEqual(habit.time.strftime('%H:%M:%S'), data['time'])
        self.assertEqual(habit.activity, data['activity'])
        self.assertEqual(habit.period, data['period'])
        self.assertEqual(habit.time_for_action, timedelta(
            seconds=data['time_for_action']))
        self.assertEqual(habit.is_public, data['is_public'])
        self.assertEqual(habit.is_pleasant, data['is_pleasant'])

    def test_create_wrong_time(self):
        url = reverse('habits_create')
        data = {
            'place': "тестовое место",
            'time': "19:00:00",

            'activity': "тестовая привычка",
            'period': "weekly",
            'time_for_action': 300,
            'is_pleasant': True,
            'is_public': True}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {
            "non_field_errors": [
                "Время на выполнение привычки не должно превышать 2 минуты (120 секунд)!"]
        })

    def test_create_wrong_compensation(self):
        url = reverse('habits_create')
        data = {
            'place': "тестовое место",
            'time': "19:00:00",
            'activity': "тестовая привычка",
            'period': "weekly",
            'time_for_action': 40,
            'is_pleasant': True,
            'is_public': True,
            'compensation': 'test_compensation'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {
            "non_field_errors": [
                "У приятной привычки не может быть вознаграждения и связанной приятной привычки!"]
        })

    def test_create_wrong_linked_habit(self):
        url = reverse('habits_create')
        data = {
            'place': "тестовое место",
            'time': "19:00:00",
            'activity': "тестовая привычка",
            'period': "weekly",
            'time_for_action': 40,
            'is_pleasant': True,
            'is_public': True,
            'linked_habit': self.habit.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {
            "non_field_errors": [
                "У приятной привычки не может быть вознаграждения и связанной приятной привычки!"]
        })

    def test_create_wrong_linked_habit_and_compensation(self):
        url = reverse('habits_create')
        data = {
            'place': "тестовое место",
            'time': "19:00:00",
            'activity': "полезная с вознаграждением и связанной привычкой",
            'period': "weekly",
            'time_for_action': 40,
            'is_pleasant': False,
            'is_public': True,
            'linked_habit': self.habit.id,
            'compensation': 'test_compensation'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {
            "non_field_errors": [
                "У полезной привычки не может быть одновременно вознаграждения и связанной приятной привычки!"]
        })

    def test_create_useful_wrong_linked_habit_and_compensation(self):
        url = reverse('habits_create')
        data = {
            'place': "тестовое место",
            'time': "19:00:00",
            'activity': "полезная без вознаграждения",
            'period': "weekly",
            'time_for_action': 40,
            'is_pleasant': False,
            'is_public': True}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {
            "non_field_errors": [
                'У полезной привычки должно быть вознаграждение или связанная приятная привычка!']
        })

    def test_update(self):
        url = reverse('habits_update', args=[self.habit.id])
        data = {
            'place': "обновленное место",
            'time': "21:00:00",
            'activity': "обновленное действие",
            'period': "daily",
            'time_for_action': 50,
            'is_pleasant': False,
            'compensation': 'new compensation',
            'is_public': True}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit = Habits.objects.get(pk=self.habit.pk)
        self.assertEqual(habit.place, data['place'])
        self.assertEqual(habit.time.strftime('%H:%M:%S'), data['time'])
        self.assertEqual(habit.activity, data['activity'])
        self.assertEqual(habit.period, data['period'])
        self.assertEqual(habit.time_for_action, timedelta(
            seconds=data['time_for_action']))
        self.assertEqual(habit.is_public, data['is_public'])
        self.assertEqual(habit.is_pleasant, data['is_pleasant'])

    def test_update_another_user(self):
        """
        проверяем, что созданную другим пользователем привычку нельзя обновлять
        """
        create_url = reverse('habits_create')

        create_data = {
            'place': "новое место",
            'time': "10:00:00",
            'activity': "новая активность",
            'period': "weekly",
            'time_for_action': 30,
            'is_pleasant': False,
            'compensation': 'компенсация',
            'is_public': False
        }
        # Создаем новую привычку
        response = self.client.post(create_url, create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Получение ID созданной привычки
        habit_id = response.json().get('id')


        # Создаем второго пользователя
        self.user2 = TestUser.create_user2()

        data2 = {"chat_id": self.user2.chat_id,
                "password": TEST_USER_PASSWORD2
                }
        # получаем  токен для второго пользователя и добавляем его в заголовок
        response = self.client.post(self.url_token, data2)
        self.access_token2 = response.json().get('access')
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token2}')

        # Обновление привычки с помощью второго пользователя
        update_url = reverse('habits_update', args=[habit_id])
        update_data = {
            'place': "измененное место",
            'time': "12:00:00",
            'activity': "изменненая активность",
            'period': "daily",
            'time_for_action': 40,
            'is_pleasant': False,
            'compensation': 'измененная компенсация',
            'is_public': True
        }
        update_response = self.client.patch(update_url, update_data)


        self.assertEqual(update_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(update_response.json().get('detail'), 'У вас недостаточно прав для выполнения данного действия.')

    def test_delete(self):
        delete_habit = Habits.objects.create(
            user=self.user,
            place="публичная",
            time="13:00:00",
            activity="публичная",
            period="weekly",
            time_for_action=timedelta(seconds=40),
            is_public=True
        )
        number = Habits.objects.all().count()
        url = reverse('habits_destroy', args=[delete_habit.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habits.objects.count(), number - 1)

    def test_get(self):
        response = self.client.get(reverse("habits_retrieve", args=[self.habit.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habits_public_list(self):
        habit = Habits.objects.create(
            user=self.user,
            place="публичная",
            time="13:00:00",
            activity="публичная",
            period="weekly",
            time_for_action=timedelta(seconds=40),
            is_public=True
        )
        response = self.client.get(reverse("habits_public_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_check_owner(self):
        """
        Проверяем, что user-ом стал пользователь, создавший привычку
        """
        url = reverse('habits_create')
        data = {
            'place': "проверка пользователя",
            'time': "19:00:00",
            'activity': "тестовая привычка",
            'period': "weekly",
            'time_for_action': 40,
            'is_pleasant': True,
            'is_public': True}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Получение ID пользователя
        user_id = response.data['user']

        # Получение ID созданной привычки
        habit_id = response.json().get('id')
        habit = Habits.objects.get(pk=habit_id)
        user = User.objects.get(id=user_id)
        self.assertEqual(habit.user, user)