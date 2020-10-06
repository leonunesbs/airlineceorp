from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from geopy import distance


class Route(models.Model):
    departure = models.ForeignKey('airports.Airport', on_delete=models.CASCADE, related_name='departure', help_text='Saída')
    arrival = models.ForeignKey('airports.Airport', on_delete=models.CASCADE, related_name='arrival', help_text='Chegada')
    distance = models.FloatField(help_text='Distância em Nm')

    rate = models.FloatField(default=1.0)


    def __str__(self):
        return f'{self.departure.icao}{self.arrival.icao}'


    def calculate_distance(self):
        # Calcula a distancia entre as coordenadas do Departure e as coordenadas do Arrival
        d = distance.great_circle(self.departure.coordinates, self.arrival.coordinates).nm
        return d

    def calculate_rate(self):
        # Calcula o rate da Rota
        d_rate = self.departure.rate
        a_rate = self.arrival.rate
        return d_rate * a_rate

    @receiver(pre_save, sender='routes.Route')
    # Receives SIGNAL que define a distancia entre os aeroportos
    def set_distance(sender, instance, **kwargs):
        instance.distance = instance.calculate_distance()

    @receiver(pre_save, sender='routes.Route')
    # Receives SIGNAL que define o rate da rota 
    def set_rate(sender, instance, **kwargs):
        instance.rate = instance.calculate_rate()
