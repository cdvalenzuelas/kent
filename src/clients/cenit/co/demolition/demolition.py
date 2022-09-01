import pandas as pd

from src.clients.cenit.co.utils.utils import common_index, def_note
from src.clients.cenit.co.demolition.cleaner import demolition_cleaner
from src.clients.cenit.co.demolition.description import def_demolition_description


# (VALEC17) Define la cantidad de los elementos nuevos
def def_qty(row):
    qty_x, qty_y = row

    if qty_y == '-':
        return qty_x
    else:
        return qty_y


# (VALEC17) OJO EL DEMOLITION TAMBIÉN PUEDE VENIR EN FORMA DE MTO
def demolition(method, co_df, piping_class):
    # (VALEC17) Leer el archivo de demolición
    demolition_df = pd.read_csv('./inputs/demolition.csv')

    print('💡 VERIFICAR QUE EL ARCHIVO demolition.csv SEA EL CORRECTO\n')

    # (VALEC17) Limpiar el demolition.csv
    demolition_df = demolition_cleaner(demolition_df, piping_class)

    # (VALEC17) Definir el demolition descrption según el type
    demolition_df['DEMOLITION_DESCRIPTION'] = demolition_df[[
        'LINE_NUM', 'TYPE', 'DEMOLITION_DESCRIPTION', 'WEIGHT', 'UNDERGROUND', 'FORGIVEN']].apply(def_demolition_description, axis=1, method=method)

    # (VALEC17) Se suman las cantidades
    demolition_df = demolition_df.groupby(['DEMOLITION_DESCRIPTION'], as_index=False)[
        ['WEIGHT']].agg(WEIGHT=('WEIGHT', sum))

    # (VALEC17) Crear índices comunes para hacer un merge
    demolition_df['common_index'] = demolition_df['DEMOLITION_DESCRIPTION'].apply(
        common_index)

    co_df['common_index'] = co_df['DESCRIPTION'].apply(
        common_index)

    # (VALEC17) Hacer un merge full
    co_df = pd.merge(
        co_df, demolition_df, on='common_index', how='outer')

    # (VALEC17) Llenar espacios vacío
    co_df.fillna('-', inplace=True)

    # (VALEC17) Definir las cantidades
    co_df['QTY'] = co_df[[
        'QTY', 'WEIGHT']].apply(def_qty, axis=1)

    # (VALEC17) Deninir si un elemento es nuevo o no
    co_df['NOTE'] = co_df[[
        'AREA', 'NOTE']].apply(def_note, axis=1)

    # (VALEC17) Eliminando columnas inncesarias
    co_df.drop(['common_index', 'DEMOLITION_DESCRIPTION',
                'WEIGHT'], inplace=True, axis=1)

    # (VALEC17) Guardar el archivo creado
    return co_df
