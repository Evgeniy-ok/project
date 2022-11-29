from django.db import models

class Posts(models.Model):
    name = models.CharField(max_length=100)
    breed = models.TextField()
    age = models.IntegerField()
    image = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.name