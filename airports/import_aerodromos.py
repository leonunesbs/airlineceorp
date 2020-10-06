import csv
from airports.models import Airport
from lat_lon_parser import parse as lat_lon_parser

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