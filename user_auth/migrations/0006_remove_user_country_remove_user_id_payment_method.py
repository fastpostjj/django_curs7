# Generated by Django 4.2.3 on 2023-08-06 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0005_user_chat_id_user_is_subscripted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='country',
        ),
        migrations.RemoveField(
            model_name='user',
            name='id_payment_method',
        ),
    ]
