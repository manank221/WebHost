# Generated by Django 5.2.3 on 2025-06-20 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmessage',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
