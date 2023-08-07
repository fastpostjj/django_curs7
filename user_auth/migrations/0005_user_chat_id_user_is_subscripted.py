# Generated by Django 4.2.3 on 2023-08-06 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0004_remove_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='chat_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='chat_id'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_subscripted',
            field=models.BooleanField(default=False, verbose_name='Подписан'),
        ),
    ]