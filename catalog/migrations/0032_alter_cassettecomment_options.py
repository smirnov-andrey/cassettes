# Generated by Django 4.1.7 on 2023-06-28 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0031_alter_cassettecomment_cassette_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cassettecomment',
            options={'ordering': ('-created',), 'verbose_name': 'Cassette comment', 'verbose_name_plural': 'Cassette comments'},
        ),
    ]