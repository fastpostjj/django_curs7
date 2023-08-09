from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from habits.models import Habits_pleasant, Habits_useful
from user_auth.models import User

# Create your tests here.
TEST_CHAT_ID_ADMIN = 10
TEST_CHAT_ID_USER = 11
TEST_CHAT_ID_STAFF = 12

TEST_ADMIN_PASSWORD = '123abc123'
TEST_USER_PASSWORD = '124abc124'
TEST_STAFF_PASSWORD = '125abc125'


class TestUser():

    def create_user(self, *args, **kwargs):
        self.user = User.objects.create(
            chat_id=TEST_CHAT_ID_USER,
            first_name='Test',
            last_name='Just User',
            is_staff=False,
            is_superuser=False
        )
        self.user.set_password(TEST_USER_PASSWORD)
        self.user.save()
        return self.user

    def create_staff(self, *args, **kwargs):
        self.user = User.objects.create(
            chat_id=TEST_CHAT_ID_STAFF,
            first_name='Test',
            last_name='Staff',
            is_staff=True,
            is_superuser=False
        )
        self.user.set_password(TEST_STAFF_PASSWORD)
        self.user.save()
        return self.user

    def create_admin(self, *args, **kwargs):
        self.user = User.objects.create(
            chat_id=TEST_CHAT_ID_ADMIN,
            first_name='Test',
            last_name='Admin',
            is_staff=True,
            is_superuser=True
        )
        self.user.set_password(TEST_ADMIN_PASSWORD)
        self.user.save()
        return self.user


class TestHabitsPleasant(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = TestUser.create_user()
        self.url_token = reverse('token_obtain_pair')
        response = self.client.post(self.url_token,
                                    {"chat_id": self.user.chat_id,
                                     "password": self.user.password
                                     })
        self.access_token = response.json().get('access')
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.habit_pleasant = Habits_pleasant.objects.create(
            user=self.user,
            place="театре",
            time="19:00:00",
            activity="смотреть спектакль",
            period="weekly",
            time_for_action=40,
            is_public=True
        )
        self.habit_pleasant.save()
    # compensation
    #   linked_habit
    def test_habit_pleasant_create(self):
        number = Habits_pleasant.objects.all().count()
        url = reverse('habits_pleasant_create')
        data = {'user': self.user.chat_id,
                'place': "тестовое место",
                'time': "19:00:00",
                'activity': "тестовая привычка",
                'period': "weekly",
                'time_for_action': 40,
                'is_public': True}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habits_pleasant.objects.count(), number + 1)
        habit = Habits_pleasant.objects.order_by('id').last()[0]
        self.assertEqual(habit.place, data['place'])
        self.assertEqual(habit.time, data['time'])
        self.assertEqual(habit.activity, data['activity'])
        self.assertEqual(habit.period, data['period'])
        self.assertEqual(habit.time_for_action, data['time_for_action'])
        self.assertEqual(habit.is_public, data['is_public'])

    #         self.habit_pleasant2 = Habits_pleasant.objects.create(
    #         user=self.user,
    #         place="тестовое место",
    #         time="19:00:00",
    #         activity="тестовая привычка",
    #         period="weekly",
    #         time_for_action=40,
    #         is_public=True
    #     )