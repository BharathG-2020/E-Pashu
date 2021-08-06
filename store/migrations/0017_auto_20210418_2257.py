# Generated by Django 3.1.7 on 2021-04-18 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_auto_20210418_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='address',
            field=models.TextField(blank=True, help_text='Required', verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='animal',
            name='description',
            field=models.TextField(blank=True, help_text='Required', verbose_name='description'),
        ),
    ]
