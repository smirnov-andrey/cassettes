# Generated by Django 4.1.7 on 2023-08-08 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_collectorfeedback'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='collectorfeedback',
            constraint=models.UniqueConstraint(fields=('user', 'collector'), name='unique_feedback'),
        ),
        migrations.AddConstraint(
            model_name='collectorfeedback',
            constraint=models.CheckConstraint(check=models.Q(('user', models.F('collector'))), name='self_feedback'),
        ),
    ]