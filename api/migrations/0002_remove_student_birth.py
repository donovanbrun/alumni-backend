# Generated by Django 4.0.4 on 2022-06-21 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='birth',
        ),
    ]
