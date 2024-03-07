from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    pesel = models.IntegerField()

    def __str__(self):
        return f'{self.name} {self.last_name}'

