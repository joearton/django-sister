# Generated by Django 3.2.9 on 2022-03-14 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sister', '0008_auto_20220312_1039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sdm',
            name='gs_url',
        ),
        migrations.RemoveField(
            model_name='sdm',
            name='scopus_id',
        ),
        migrations.RemoveField(
            model_name='sdm',
            name='sinta_id',
        ),
        migrations.AddField(
            model_name='unit',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='sister.unit'),
        ),
    ]
