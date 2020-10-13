from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


DAYS = (
    ('0', 'Domingo'),
    ('1', 'Segunda-feira'),
    ('2', 'Terça-feira'),
    ('3', 'Quarta-feira'),
    ('4', 'Quinta-feira'),
    ('5', 'Sexta-feira'),
    ('6', 'Sábado'),
)


class Flight(models.Model):
    # Configura um novo Voo
    airline = models.ForeignKey('airlines.Airline', on_delete=models.CASCADE)
    aircraft = models.ForeignKey(
        'aircrafts.Aircraft', on_delete=models.CASCADE)
    route = models.ForeignKey('routes.Route', on_delete=models.CASCADE)

    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    repeat = models.ManyToManyField('Repeat')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Repeat(models.Model):
    day = models.CharField(max_length=1, choices=DAYS, primary_key=True)

    def __str__(self):
        return self.get_day_display()

    class Meta:
        ordering = ['day']


@receiver(post_save, sender='flights.Repeat')
# Carrega todos os dias ao salvar um único dia
def load_days(sender, **kwargs):
    for day in DAYS:
        Repeat.objects.get_or_create(day=day[0])
