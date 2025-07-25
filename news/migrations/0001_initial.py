# Generated by Django 5.2.3 on 2025-06-24 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewsArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
                ('content', models.TextField()),
                ('publication_date', models.DateTimeField(auto_now_add=True)),
                ('category', models.CharField(choices=[('international', 'International'), ('national', 'National'), ('tech', 'Tech'), ('sports', 'Sports')], max_length=20)),
                ('image', models.ImageField(blank=True, null=True, upload_to='news_images/')),
            ],
            options={
                'ordering': ['-publication_date'],
            },
        ),
    ]
