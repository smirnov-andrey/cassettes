# Generated by Django 4.1.7 on 2023-06-19 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0028_remove_cassettefrequencyresponse_cassette_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cassetteprice',
            name='condition',
        ),
        migrations.RemoveField(
            model_name='cassetteprice',
            name='price',
        ),
        migrations.AddField(
            model_name='cassetteprice',
            name='excellent',
            field=models.IntegerField(blank=True, null=True, verbose_name='Excellent price'),
        ),
        migrations.AddField(
            model_name='cassetteprice',
            name='good',
            field=models.IntegerField(blank=True, null=True, verbose_name='Good price'),
        ),
        migrations.AddField(
            model_name='cassetteprice',
            name='mint',
            field=models.IntegerField(blank=True, null=True, verbose_name='Mint price'),
        ),
        migrations.AddField(
            model_name='cassetteprice',
            name='near_mint',
            field=models.IntegerField(blank=True, null=True, verbose_name='Near mint price'),
        ),
        migrations.AddField(
            model_name='cassetteprice',
            name='poor',
            field=models.IntegerField(blank=True, null=True, verbose_name='Poor price'),
        ),
        migrations.AddField(
            model_name='cassetteprice',
            name='very_good',
            field=models.IntegerField(blank=True, null=True, verbose_name='Very good price'),
        ),
    ]
