import pandas as pd


from src.utils.normalize_string import normalize_string


def def_qty(row, cell, total):
    description, qty = row

    if normalize_string(description) == cell:
        return total
    else:
        return qty


def pipes_hidrostatic_test():
    # Leer el MTO limpio
    co_df = pd.read_csv('./output/mto.csv')

    # Obtener únicamente las columnas innecesarias
    co_df = co_df[['TYPE', 'TYPE_CODE', 'FIRST_SIZE_NUMBER', 'QTY']]

    # Deajr únicamente las tuberías
    co_df = co_df[(co_df['TYPE'] == 'PP')]

    # Multiplicar el diámetro por la longitud
    co_df['TOTAL'] = co_df['QTY'] * co_df['FIRST_SIZE_NUMBER']

    # Sacar la sumatoria
    total = co_df['TOTAL'].sum()*1.05

    # Definir el sitio en el que se pone la cantidad
    cell = normalize_string('PRUEBA HIDROSTÁTICA DE TUBERÍA')

    # Leer el archivo de cantidades de obra creadas
    co_template = pd.read_csv('./output/co.csv')

    # Encontral la celda y colocar el valor
    co_template['QTY'] = co_template[[
        'DESCRIPTION', 'QTY']].apply(def_qty, axis=1, args=(cell, total))

    # Guardar el archivo creado
    co_template.to_csv('./output/co.csv', index=False)
