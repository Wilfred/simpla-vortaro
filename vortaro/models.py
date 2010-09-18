from django.db import models

class Word(models.Model):
    word = models.CharField(max_length=50)
