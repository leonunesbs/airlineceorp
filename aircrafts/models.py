from django.db import models
from django.contrib.auth.models import User


class Aircraft(models.Model):
    # Modelo de características técnicas de cada aeronave

    CATEGORY = (
        ('C', 'Cargo'),
        ('P', 'Passengers'),
    )

    icao24 = models.CharField(
        max_length=6, help_text='Código obtido no Opensky Network')
    manufacturer = models.CharField(max_length=30, help_text='Fabricante')
    model = models.CharField(max_length=15, help_text='Modelo')

    range = models.IntegerField(help_text='Alcance')
    category = models.CharField(max_length=1, choices=CATEGORY)

    cargo_capacity = models.FloatField(help_text='Nº máx de Cargo em Kg')
    passengers_capacity = models.IntegerField(
        help_text='Nº máx de Passageiros')
    fuel_capacity = models.FloatField(
        help_text='Capacidade de combustível em Kg')

    cruise_altitude = models.IntegerField(
        help_text='Altitude de cruseiro em Feets')
    cruise_speed = models.IntegerField(
        help_text='Velocidade de cruseiro em Knots')

    def __str__(self):
        return f'{self.manufacturer} {self.model}'


class State(models.Model):
    aircraft = models.ForeignKey(
        'Aircraft',
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text='Dono da aeronave'
    )
    pax = models.IntegerField(
        default=0,
        help_text='N° de passageiros a bordo',
    )
    cargo = models.IntegerField(
        default=0,
        help_text='Kg de Cargo a bordo',
    )
    fuel = models.FloatField(
        default=0,
        help_text='Kg de Combustível a bordo',
    )
