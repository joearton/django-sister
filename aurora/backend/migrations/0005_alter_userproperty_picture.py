# Generated by Django 3.2.9 on 2022-03-09 03:44

import aurora.backend.library.models.renamer
import aurora.backend.library.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_alter_userproperty_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userproperty',
            name='picture',
            field=models.ImageField(blank=True, help_text=aurora.backend.library.validators.Validators.help_text, null=True, upload_to=aurora.backend.library.models.renamer.BaseModelRenamer.by_automatic_protected, validators=[aurora.backend.library.validators.Validators.validate], verbose_name='Picture'),
        ),
    ]
