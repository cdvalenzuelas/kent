import pandas as pd


from src.utils.normalize_string import normalize_string


def def_qty(row, cell, total):
    description, qty = row

    if normalize_string(description) == cell:
        return total
    else:
        return qty


def pipes_hidrostatic_test(mto_df, co_df):
    # Obtener únicamente las columnas innecesarias
    mto_df = mto_df[['TYPE', 'TYPE_CODE', 'FIRST_SIZE_NUMBER', 'QTY']]

    # Deajr únicamente las tuberías
    mto_df = mto_df[(mto_df['TYPE'] == 'PP')]

    # Multiplicar el diámetro por la longitud
    mto_df['TOTAL'] = mto_df['QTY'] * mto_df['FIRST_SIZE_NUMBER']

    # Sacar la sumatoria
    total = mto_df['TOTAL'].sum()*1.05

    # Definir el sitio en el que se pone la cantidad
    cell = normalize_string('PRUEBA HIDROSTÁTICA DE TUBERÍA')

    # Encontral la celda y colocar el valor
    co_df['QTY'] = co_df[[
        'DESCRIPTION', 'QTY']].apply(def_qty, axis=1, args=(cell, total))

    # Guardar el archivo creado
    return co_df
