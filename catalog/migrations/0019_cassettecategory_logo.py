# Generated by Django 4.1.7 on 2023-05-03 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_cassettebrand_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='cassettecategory',
            name='logo',
            field=models.ImageField(blank=True, upload_to='category_logo'),
        ),
    ]