from math import pi
import pandas as pd

from src.utils.normalize_string import normalize_string


# Calcular el área total
def def_total_area(row):
    type_element, qty, area = row

    if type_element == '-':
        return 0

    qty = float(qty)
    area = float(area)

    if type_element == 'PP':
        return pi*area*qty/1000
    else:
        return area * qty

# Insertar el valor calculado en el documento de cantidades de obra


def def_qty(row, cells_list, total):
    description, qty = row

    if normalize_string(description) in cells_list:
        return total
    else:
        return qty


def areas():
    # Leer el MTO limpio
    co_df = pd.read_csv('./output/mto.csv')

    # Obtener únicamente las columnas innecesarias
    co_df = co_df[['TYPE', 'TYPE_CODE', 'QTY', 'AREA']]

    # Definir área total
    co_df['TOTAL_AREA'] = co_df[['TYPE', 'QTY', 'AREA']].apply(
        def_total_area, axis=1)

    # Calcular el área total
    total = round(co_df['TOTAL_AREA'].sum(), 2)

    # Insertar el valor calculado en el documento de cantidades de obra

    cell_1 = normalize_string(
        'LIMPIEZA CON CHORRO DE ABRASIVO GRADO METAL CASI BLANCO SEGÚN NORMA SSPC-SP 10')
    cell_2 = normalize_string(
        'SUMINISTRO Y APLICACIÓN DE PINTURA PRIMER, BASE ANTICORROSIVA O IMPRIMANTE E= 6–10 MILS')
    cell_3 = normalize_string(
        'SUMINISTRO Y APLICACIÓN DE PINTURA EPÓXICA POLIAMINA DE BARRERA E= 6–8 MILS')
    cell_4 = normalize_string(
        'SUMINISTRO Y APLICACIÓN DE PINTURA POLIURETANO ALIFÁTICO DE ACABADO E=5–7 MILS')

    # Estos son las celdas en donde se insertará el total de área
    cells_list = [cell_1, cell_2, cell_3, cell_4]

    # Leer el archivo de cantidades de obra creadas
    co_template = pd.read_csv('./output/co.csv')

    # Encontral la celda y colocar el valor
    co_template['QTY'] = co_template[[
        'DESCRIPTION', 'QTY']].apply(def_qty, axis=1, args=(cells_list, total))

    # Guardar el archivo creado
    co_template.to_csv('./output/co.csv', index=False)
