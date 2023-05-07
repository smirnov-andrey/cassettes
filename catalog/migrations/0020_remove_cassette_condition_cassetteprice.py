# Generated by Django 4.1.7 on 2023-05-05 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0019_cassettecategory_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cassette',
            name='condition',
        ),
        migrations.CreateModel(
            name='CassettePrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(verbose_name='price')),
                ('condition', models.CharField(choices=[('mint', 'Mint'), ('excellent', 'Excellent'), ('very_good', 'Very good'), ('good', 'Good'), ('poor', 'Poor')], max_length=100, verbose_name='condition')),
                ('cassette', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.cassette', verbose_name='cassette')),
            ],
            options={
                'verbose_name': 'Add cassette price',
                'verbose_name_plural': 'Cassettes prices',
            },
        ),
    ]