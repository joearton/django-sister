# Generated by Django 3.2.9 on 2022-03-09 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sister', '0004_alter_sdm_nidn'),
    ]

    operations = [
        migrations.AddField(
            model_name='sdm',
            name='slugname',
            field=models.SlugField(default=1, max_length=128, unique=True, verbose_name='ID Unik'),
            preserve_default=False,
        ),
    ]
