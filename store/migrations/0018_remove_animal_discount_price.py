# Generated by Django 3.1.7 on 2021-04-18 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_auto_20210418_2257'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='animal',
            name='discount_price',
        ),
    ]
