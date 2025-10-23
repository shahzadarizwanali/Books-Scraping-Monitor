from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100)
    price_including_tax = models.DecimalField(max_digits=8, decimal_places=2)
    price_excluding_tax = models.DecimalField(max_digits=8, decimal_places=2)
    availability = models.CharField(max_length=100)
    num_reviews = models.IntegerField(default=0)
    rating = models.CharField(max_length=20)
    image_url = models.URLField()
    page_url = models.URLField(unique=True)
    crawl_timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="active")
    source_url = models.URLField(blank=True, null=True)
    raw_html = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
