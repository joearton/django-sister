# Generated by Django 3.2.9 on 2022-03-09 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sister', '0003_alter_sdm_nip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sdm',
            name='nidn',
            field=models.CharField(blank=True, max_length=16, null=True, unique=True, verbose_name='NIDN'),
        ),
    ]
