# Generated by Django 4.1.7 on 2023-08-09 15:22

from django.db import migrations
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_collectorfeedback_feedback'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', users.models.UserManager()),
            ],
        ),
    ]