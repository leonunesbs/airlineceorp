from django.db import models
from django.contrib.auth.models import User

class Aircraft(models.Model):
    manufacturer = models.CharField(max_length=30, help_text='Fabricante')
    model = models.CharField(max_length=15, help_text='Modelo')

    def __str__(self):
        return f'{self.manufacturer} {self.model}'


class Characteristic(models.Model):
    # Modelo de características técnicas de cada aeronave
    CATEGORY = (
        ('C', 'Cargo'),
        ('P', 'Passengers'),
    )
    aircraft = models.OneToOneField('Aircraft', on_delete=models.CASCADE)
    range = models.IntegerField(help_text='Alcance')
    category = models.CharField(max_length=1, choices=CATEGORY)
    max_cargo = models.FloatField(help_text='Nº máx de Cargo em Kg')
    max_passengers = models.IntegerField(help_text='Nº máx de Passageiros')

    def __str__(self):
        return f'{self.aircraft.manufacturer} {self.aircraft.model}'



class State(models.Model):
    aircraft = models.ForeignKey('Aircraft', on_delete=models.CASCADE)
    
    class Meta:
        abstract = True

class OwnerState(State):
    owner = models.ForeignKey('companies.Company', on_delete=models.CASCADE)

class LoadState(State):
    pax = models.IntegerField(help_text='N° de passageiros a bordo')
    cargo = models.IntegerField(help_text='Kg de Cargo a bordo')
