import pandas as pd

from src.clients.cenit.co.utils.utils import common_index, def_note
from src.clients.cenit.co.demolition.cleaner import demolition_cleaner
from src.clients.cenit.co.demolition.description import def_demolition_description


# Define la cantidad de los elementos nuevos
def def_qty(row):
    qty_x, qty_y = row

    if qty_y == '-':
        return qty_x
    else:
        return qty_y


# OJO EL DEMOLITION TAMBIÉN PUEDE VENIR EN FORMA DE MTO
def demolition(method, co_df, piping_class):
    # Leer el archivo de demolición
    demolition_df = pd.read_csv('./inputs/demolition.csv')

    print('💡 VERIFICAR QUE EL ARCHIVO demolition.csv SEA EL CORRECTO\n')

    # Limpiar el demolition.csv
    demolition_df = demolition_cleaner(demolition_df, piping_class)

    # Definir el demolition descrption según el type
    demolition_df['DEMOLITION_DESCRIPTION'] = demolition_df[[
        'LINE_NUM', 'TYPE', 'DEMOLITION_DESCRIPTION', 'WEIGHT', 'UNDERGROUND', 'FORGIVEN']].apply(def_demolition_description, axis=1, method=method)

    # Se suman las cantidades
    demolition_df = demolition_df.groupby(['DEMOLITION_DESCRIPTION'], as_index=False)[
        ['WEIGHT']].agg(WEIGHT=('WEIGHT', sum))

    # Crear índices comunes para hacer un merge
    demolition_df['common_index'] = demolition_df['DEMOLITION_DESCRIPTION'].apply(
        common_index)

    co_df['common_index'] = co_df['DESCRIPTION'].apply(
        common_index)

    # Hacer un merge full
    co_df = pd.merge(
        co_df, demolition_df, on='common_index', how='outer')

    # Llenar espacios vacío
    co_df.fillna('-', inplace=True)

    # Definir las cantidades
    co_df['QTY'] = co_df[[
        'QTY', 'WEIGHT']].apply(def_qty, axis=1)

    # Deninir si un elemento es nuevo o no
    co_df['NOTE'] = co_df[[
        'AREA', 'NOTE']].apply(def_note, axis=1)

    # Eliminando columnas inncesarias
    co_df.drop(['common_index', 'DEMOLITION_DESCRIPTION',
                'WEIGHT'], inplace=True, axis=1)

    # Guardar el archivo creado
    return co_df
