# Generated by Django 4.1.7 on 2023-10-07 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_cassettesort_title_en_cassettesort_title_ru'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cassettebrand',
            options={'ordering': ('title',), 'verbose_name': 'brand', 'verbose_name_plural': 'brands'},
        ),
        migrations.AlterModelOptions(
            name='cassettecollection',
            options={'ordering': ('title',), 'verbose_name': 'Collection', 'verbose_name_plural': 'Collections'},
        ),
        migrations.AlterModelOptions(
            name='cassettemanufacturer',
            options={'ordering': ('title',), 'verbose_name': 'Manufacturer', 'verbose_name_plural': 'Manufacturers'},
        ),
        migrations.AlterModelOptions(
            name='cassettemodel',
            options={'ordering': ('title',), 'verbose_name': 'Model', 'verbose_name_plural': 'Models'},
        ),
        migrations.AlterModelOptions(
            name='cassetteseries',
            options={'ordering': ('title',), 'verbose_name': 'Series', 'verbose_name_plural': 'Series'},
        ),
        migrations.AlterModelOptions(
            name='cassettesort',
            options={'ordering': ('title',), 'verbose_name': 'sort', 'verbose_name_plural': 'sorts'},
        ),
        migrations.AlterModelOptions(
            name='cassettetapelength',
            options={'ordering': ('tape_length',), 'verbose_name': 'tape length', 'verbose_name_plural': 'tape lengtes'},
        ),
        migrations.AlterModelOptions(
            name='cassettetechnology',
            options={'ordering': ('title',), 'verbose_name': 'Technology', 'verbose_name_plural': 'Technologies'},
        ),
        migrations.AlterModelOptions(
            name='cassettetype',
            options={'ordering': ('title',), 'verbose_name': 'Type', 'verbose_name_plural': 'Types'},
        ),
    ]