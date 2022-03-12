# Generated by Django 3.2.9 on 2022-03-12 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sister', '0007_sdm_metadata'),
    ]

    operations = [
        migrations.AddField(
            model_name='sdm',
            name='gs_url',
            field=models.URLField(blank=True, null=True, verbose_name='Google Scholar'),
        ),
        migrations.AddField(
            model_name='sdm',
            name='scopus_id',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Scopus ID'),
        ),
        migrations.AddField(
            model_name='sdm',
            name='sinta_id',
            field=models.CharField(blank=True, max_length=8, null=True, verbose_name='Sinta ID'),
        ),
    ]
