from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.name
        