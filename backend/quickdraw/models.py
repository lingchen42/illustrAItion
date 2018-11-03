from django.db import models

class Drawing(models.Model):
    countrycode = models.CharField(max_length=2, default='')
    drawing = models.CharField(max_length=5000, default='')
    word = models.CharField(max_length=20, default='')
    strokes = models.IntegerField(default=0)