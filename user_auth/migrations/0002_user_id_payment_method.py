# Generated by Django 4.2.3 on 2023-08-01 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='id_payment_method',
            field=models.IntegerField(blank=True, null=True, verbose_name='id метода платежа'),
        ),
    ]