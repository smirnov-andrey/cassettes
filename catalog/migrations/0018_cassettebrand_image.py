# Generated by Django 4.1.7 on 2023-05-03 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0017_cassettebrand_description_alter_cassette_brand_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cassettebrand',
            name='image',
            field=models.ImageField(blank=True, upload_to='brands', verbose_name='image'),
        ),
    ]