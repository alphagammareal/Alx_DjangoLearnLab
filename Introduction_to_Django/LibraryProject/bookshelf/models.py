from django.db import models

# Create your models here.
class book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

def _str_(self):
    return self.title
    