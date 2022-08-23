from math import pi
import pandas as pd

from src.utils.normalize_string import normalize_string

# (VALEC17) Insertar el valor calculado en el documento de cantidades de obra


def def_qty(row, cells_list, total):
    description, qty = row

    if normalize_string(description) in cells_list:
        return total
    else:
        return qty


def areas(mto_df, co_df):
    # (VALEC17) Hacer copias de los dataframes
    mto_df = mto_df.copy()
    co_df = co_df.copy()

    # (VALEC17) Calcular el área total
    total = round(mto_df['AREA'].sum(), 2)

    # (VALEC17) Insertar el valor calculado en el documento de cantidades de obra
    cell_1 = normalize_string(
        'LIMPIEZA CON CHORRO DE ABRASIVO GRADO METAL CASI BLANCO SEGÚN NORMA SSPC-SP 10')
    cell_2 = normalize_string(
        'SUMINISTRO Y APLICACIÓN DE PINTURA PRIMER, BASE ANTICORROSIVA O IMPRIMANTE E= 6–10 MILS')
    cell_3 = normalize_string(
        'SUMINISTRO Y APLICACIÓN DE PINTURA EPÓXICA POLIAMINA DE BARRERA E= 6–8 MILS')
    cell_4 = normalize_string(
        'SUMINISTRO Y APLICACIÓN DE PINTURA POLIURETANO ALIFÁTICO DE ACABADO E=5–7 MILS')

    # (VALEC17) Estos son las celdas en donde se insertará el total de área
    cells_list = [cell_1, cell_2, cell_3, cell_4]

    # (VALEC17) Encontral la celda y colocar el valor
    co_df['QTY'] = co_df[[
        'DESCRIPTION', 'QTY']].apply(def_qty, axis=1, args=(cells_list, total))

    # (VALEC17) Guardar el archivo creado
    return co_df
