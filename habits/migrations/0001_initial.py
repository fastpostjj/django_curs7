# Generated by Django 4.2.3 on 2023-08-07 06:13

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.IntegerField(blank=True, null=True, verbose_name='chat_id')),
                ('phone', models.CharField(blank=True, max_length=35, null=True, verbose_name='телефон')),
                ('is_subscripted', models.BooleanField(default=False, verbose_name='Подписан')),
            ],
            options={
                'verbose_name': 'пользователь телеграма',
                'verbose_name_plural': 'пользователи телеграма',
            },
        ),
        migrations.CreateModel(
            name='Habits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.CharField(max_length=200, verbose_name='Действие')),
                ('time', models.TimeField(verbose_name='Время')),
                ('place', models.CharField(blank=True, max_length=150, null=True, verbose_name='Место')),
                ('period', models.CharField(choices=[('every 15 minutes', 'каждые 15 минут'), ('hourly', 'ежечасно'), ('daily', 'ежедневно'), ('weekly', 'еженедельно')], default='daily', max_length=16, verbose_name='Периодичность')),
                ('time_for_action', models.DurationField(default=datetime.timedelta(seconds=120), verbose_name='Время на выполнение')),
                ('is_pleasant', models.CharField(choices=[('is_pleasant', 'приятная'), ('is_useful', 'полезная')], default='is_useful', max_length=11, verbose_name='Приятная/полезная привычка')),
                ('is_public', models.BooleanField(default=False, verbose_name='Публичная')),
                ('compensation', models.CharField(blank=True, max_length=200, null=True, verbose_name='Вознаграждение за полезную привычку')),
                ('linked_habit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='habits.habits', verbose_name='Связанная приятная привычка')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'привычка',
                'verbose_name_plural': 'привычки',
                'unique_together': {('user', 'place', 'period', 'activity')},
            },
        ),
    ]
