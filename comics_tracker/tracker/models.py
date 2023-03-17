from django.db import models

# Create your models here.

class Book(models.Model):
    rating = models.IntegerField(null=True, blank=True)
    comic_vine_id = models.IntegerField(blank=False)
    series_title = models.CharField(max_length=150, blank=False)
    issue_number = models.IntegerField(blank=False)
    issue_name = models.CharField(max_length=150, blank= False)