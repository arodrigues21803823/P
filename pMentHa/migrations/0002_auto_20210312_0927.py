# Generated by Django 3.1.6 on 2021-03-12 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pMentHa', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='disease2',
            field=models.TextField(blank=True, max_length=258),
        ),
    ]
