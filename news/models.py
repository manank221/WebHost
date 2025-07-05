from django.db import models
from django.utils.text import slugify

class NewsArticle(models.Model):
    CATEGORY_CHOICES = [
        ('international', 'International'),
        ('national', 'National'),
        ('tech', 'Tech'),
        ('sports', 'Sports'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publication_date']
