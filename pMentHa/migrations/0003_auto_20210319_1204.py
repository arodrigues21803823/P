# Generated by Django 3.1.6 on 2021-03-19 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pMentHa', '0002_auto_20210312_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='statement',
            field=models.TextField(max_length=1000),
        ),
    ]