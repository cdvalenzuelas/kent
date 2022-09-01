import pandas as pd


from src.clients.cenit.co.utils.utils import common_index, def_note, def_description
from src.clients.cenit.co.erection.def_erection_description import def_erection_description


# (VALEC17) Define la cantidad de los elementos nuevos
def def_qty(row):
    qty_x, qty_y, total_weight, unit = row

    if qty_y != '-':
        if unit == 'KG':
            return total_weight
        else:
            return qty_y

    return qty_x


def erection(mto_df, co_df):
    # (VALEC17) Hacer una copia del df
    mto_df = mto_df.copy()

    # (VALEC17) Extraer únicamente las columnas necesarias
    mto_df = mto_df[['TYPE', 'ERECTION_DESCRIPTION',
                     'TOTAL_WEIGHT', 'QTY', 'UNDERGROUND', 'PRE_MANUFACTURING']]

    # (VALEC17) Redefnir la descripción del montaje en función de si está enterrada o aérea
    mto_df['ERECTION_DESCRIPTION'] = mto_df[[
        'ERECTION_DESCRIPTION', 'UNDERGROUND', 'PRE_MANUFACTURING']].apply(def_erection_description, axis=1)

    # (VALEC17) Se suman las cantidades
    mto_df = mto_df.groupby(['ERECTION_DESCRIPTION'], as_index=False)[
        ['TOTAL_WEIGHT', 'QTY']].agg(TOTAL_WEIGHT=('TOTAL_WEIGHT', sum), QTY=('QTY', sum))

    # (VALEC17) Crear índices comunes para hacer un merge
    mto_df['common_index'] = mto_df['ERECTION_DESCRIPTION'].apply(common_index)

    co_df['common_index'] = co_df['DESCRIPTION'].apply(
        common_index)

    # (VALEC17) Hacer un merge full
    co_df = pd.merge(co_df, mto_df, on='common_index', how='outer')

    # (VALEC17) Llenar los espacios nulos
    co_df.fillna('-', inplace=True)

    # (VALEC17) Deninir si un elemento es nuevo o no
    co_df['NOTE'] = co_df[['AREA', 'NOTE']].apply(def_note, axis=1)

    # (VALEC17) Definir descrpción
    co_df['DESCRIPTION'] = co_df[['DESCRIPTION', 'ERECTION_DESCRIPTION']].apply(
        def_description, axis=1)

    # (VALEC17) Definir las cantidades
    co_df['QTY_x'] = co_df[['QTY_x', 'QTY_y',
                            'TOTAL_WEIGHT', 'UNIT']].apply(def_qty, axis=1)

    # (VALEC17) Renombrar la columna necesaria
    co_df.rename(columns={'QTY_x': 'QTY'}, inplace=True)

    # (VALEC17) Eliminando columnas inncesarias
    co_df.drop(['common_index', 'ERECTION_DESCRIPTION',
               'TOTAL_WEIGHT', 'TOTAL_WEIGHT', 'QTY_y'], inplace=True, axis=1)

    # (VALEC17) Guardar las cantidades de obra
    return co_df
