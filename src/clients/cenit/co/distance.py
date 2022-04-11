import re
import pandas as pd


from src.clients.cenit.co.utils import common_index
from src.utils.normalize_string import normalize_string


# Definir distancia
def def_distance(row, messure, total):
    description, qty = row

    description = normalize_string(description)

    if messure <= 50 and description == normalize_string('TRANSPORTE Y ACOPIO DE TUBERÍA DISTANCIAS <= 50 KM'):
        return total
    elif messure > 50 and messure <= 120 and description == normalize_string('TRANSPORTE Y ACOPIO DE TUBERÍA DISTANCIAS 50 KM <= D <= 120 KM'):
        return total
    elif messure > 120 and messure <= 200 and description == normalize_string('TRANSPORTE Y ACOPIO DE TUBERÍA DISTANCIAS 120 KM <= D <= 200 KM'):
        return total
    elif messure > 200 and messure <= 300 and description == normalize_string('TRANSPORTE Y ACOPIO DE TUBERÍA DISTANCIAS 200 KM <= D <= 300 KM'):
        return total
    elif messure > 300 and messure >= 300 and description == normalize_string('TRANSPORTE Y ACOPIO DE TUBERÍA DISTANCIAS > 300 KM'):
        return total
    else:
        return qty


def distance(messure):
    # Leer el MTO limpio
    co_df = pd.read_csv('./output/mto.csv')

    # Calcular el peso total del proyecto
    total = round(co_df['TOTAL_WEIGHT'].sum()*messure/1000, 2)

    # Leer el archivo de cantidades de obra creadas
    co_template = pd.read_csv('./output/co.csv')

    # Definir la cantidad de TON*KM
    co_template['QTY'] = co_template[['DESCRIPTION', 'QTY']].apply(
        def_distance, axis=1, messure=messure, total=total)

    # Guardar el archivo creado
    co_template.to_csv('./output/co.csv', index=False)
