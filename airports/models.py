from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from routes.models import Route
from lat_lon_parser import parse as lat_lon_parser

AIRPORT_OPERATIONS = (
    ('I', 'IFR'),
    ('V', 'VFR'),
    ('V/I', 'VFR/IFR'),
)

class Airport(models.Model):
    icao = models.CharField(max_length=4, primary_key=True)
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    uf = models.CharField(max_length=2)
    latitude = models.FloatField()
    longitude = models.FloatField()
    length = models.FloatField()
    width = models.FloatField()
    operation_mode = models.CharField(max_length=3, choices=AIRPORT_OPERATIONS, help_text='Modo de operação')
    rate = models.FloatField(default=1.0)

    def __str__(self):
        return self.icao

    @property
    def coordinates(self):
        # Retorna (latitude, longitude)
        return (self.latitude, self.longitude)

    @receiver(post_save, sender='airports.Airport')
    # Atualiza o rate da rota sempre que o rate do Airport é alterado
    def refresh_route_rate(sender, instance, **kwargs):
        routes = Route.objects.all()
        for route in routes:
            if route.arrival.icao == instance.icao or route.departure.icao == instance.icao:
                route.rate = route.calculate_rate()
                route.save()

    # Uncomment to activate 
    # @receiver(post_delete, sender='airports.Airport')
    # SYNC AIRPORTS
    def sync_aerodromos(sender, instance, **kwargs):
        import csv

        with open('C:\\Users\\leonu\\Documents\\VSCode\\airbrasilceo\\backend\\src\\airports\\aerodromos.csv', newline='', encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                operation = 'V'
                if 'IFR' in row['OPERAÇÃO']:
                    operation = 'V/I'

                # Verifica se já existe o ICAO registrado

                Airport.objects.get_or_create(
                    icao=row['ICAO'],
                    name=row['NOME'],
                    city=row['MUNICÍPIO ATENDIDO'],
                    uf=row['UF'],
                    latitude=lat_lon_parser(row['LATITUDE']),
                    longitude=lat_lon_parser(row['LONGITUDE']),
                    operation_mode=operation,
                    length=row['COMPRIMENTO'],
                    width=row['LARGURA']
                )



class AirportLicense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text='Titular')
    airport = models.ForeignKey('Airport', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.airport.icao} | {self.user.username}'

    def set_active(self, s: bool):
        # Define se AirportLicense is_active
        self.is_active = s
        self.save()
