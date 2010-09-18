from django.db import models

class Word(models.Model):
    word = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.word
