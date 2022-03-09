# Generated by Django 3.2.9 on 2022-03-09 03:44

import aurora.backend.library.validators
import aurora.frontend.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0005_auto_20220309_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='icon',
            field=models.ImageField(blank=True, help_text=aurora.backend.library.validators.Validators.help_text, null=True, upload_to='frontend/icon', validators=[aurora.backend.library.validators.Validators.validate], verbose_name='Icon (1:1)'),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='jumbotron_bg',
            field=models.ImageField(blank=True, help_text=aurora.backend.library.validators.Validators.help_text, null=True, upload_to='frontend/', validators=[aurora.backend.library.validators.Validators.validate], verbose_name='Jumbotron Background'),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='logo',
            field=models.ImageField(blank=True, help_text=aurora.backend.library.validators.Validators.help_text, null=True, upload_to='frontend/logo', validators=[aurora.backend.library.validators.Validators.validate], verbose_name='Logo (16:9)'),
        ),
        migrations.AlterField(
            model_name='files',
            name='upload',
            field=models.FileField(help_text=aurora.backend.library.validators.Validators.help_text, max_length=1024, upload_to=aurora.frontend.models.save_file, validators=[aurora.backend.library.validators.Validators.validate], verbose_name='Upload'),
        ),
        migrations.AlterField(
            model_name='page',
            name='thumbnail',
            field=models.FileField(blank=True, help_text=aurora.backend.library.validators.Validators.help_text, null=True, upload_to='frontend/pages', validators=[aurora.backend.library.validators.Validators.validate], verbose_name='Thumbnail'),
        ),
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.FileField(blank=True, help_text=aurora.backend.library.validators.Validators.help_text, null=True, upload_to='frontend/pages', validators=[aurora.backend.library.validators.Validators.validate], verbose_name='Thumbnail'),
        ),
        migrations.AlterField(
            model_name='slideshow',
            name='image',
            field=models.ImageField(help_text=aurora.backend.library.validators.Validators.help_text, upload_to='frontend/slideshow', validators=[aurora.backend.library.validators.Validators.validate], verbose_name='Image'),
        ),
    ]
