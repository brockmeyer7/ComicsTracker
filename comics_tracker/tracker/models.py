from django.db import models

# Create your models here.

class Book(models.Model):
    marvel_id = models.IntegerField(blank=False)
    book_title = models.CharField(max_length=150, blank=False)
    issue_number = models.IntegerField(blank=False)
    description = models.TextField()
    author = models.TextField()
    artist = models.TextField()