from django.db import models

class Airline(models.Model):
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

