# Generated by Django 3.2 on 2021-05-17 01:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_question_catalogue_sex'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question_catalogue',
            name='sex',
        ),
    ]