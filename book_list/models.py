from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime as dt

# Create your models here.


class Book(models.Model):
    objects = models.Manager
    title = models.CharField(max_length=100, null=False)
    author = models.CharField(max_length=100, null=False)
    pub_date = models.IntegerField(null=True, blank=True,
                                   validators=[MinValueValidator(0), MaxValueValidator(dt.date.today().year)])
    isbn = models.IntegerField('ISBN', unique=True, null=True, blank=True)
    pages = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    cover_link = models.URLField(null=True, blank=True)
    language = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.title
