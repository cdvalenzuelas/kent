import imp
import pandas as pd


from src.utils.normalize_string import normalize_string
from src.clients.cenit.co.utils.utils import common_index, def_note


# (VALEC17) Definir cantidades
def def_qty(row):
    qty_x, qty_y = row

    return qty_x if qty_y == '-' else qty_y


# (VALEC17) Definir tags de válvulas
def def_valves_tags(size):
    if size < 2:
        return 'DEMARCACIÓN DE TUBERÍAS Y VÁLVULAS DIÁMETRO MENOR DE 2"'
    elif size >= 2 and size <= 6:
        return 'DEMARCACIÓN DE TUBERÍAS Y VÁLVULAS DIÁMETRO DE 2-6"'
    elif size >= 8 and size <= 14:
        return 'DEMARCACIÓN DE TUBERÍAS Y VÁLVULAS DIÁMETRO DE 8-14"'
    elif size >= 16 and size <= 30:
        return 'DEMARCACIÓN DE TUBERÍAS Y VÁLVULAS DIÁMETRO DE 16-30"'
    else:
        return 'DEMARCACIÓN DE TUBERÍAS Y VÁLVULAS DIÁMETRO MAYOR A 30"'


def valves_tags(mto_df, co_df):
    # (VALEC17) Traer únicamente las válvulas
    mto_df = mto_df[(mto_df['TYPE'] == 'VL')]

    # (VALEC17) Dejar únicamente las columnas necesarias
    mto_df = mto_df[['FIRST_SIZE_NUMBER', 'QTY']]

    # (VALEC17) Crear la columna tag_description
    mto_df['TAG'] = mto_df['FIRST_SIZE_NUMBER'].apply(def_valves_tags)

    # (VALEC17) Sumar las cantidades
    mto_df = mto_df.groupby(['TAG'], as_index=False)[
        ['QTY']].agg(QTY=('QTY', sum))

    # (VALEC17) Crear índice
    mto_df['common_index'] = mto_df['TAG'].apply(common_index)

    co_df['common_index'] = co_df['DESCRIPTION'].apply(
        common_index)

    # (VALEC17) Hacer el merge
    co_df = pd.merge(
        co_df, mto_df, on='common_index', how='outer')

    # (VALEC17) Llenar celdas vacías
    co_df.fillna('-', inplace=True)

    # (VALEC17) Definir las cantidades
    co_df['QTY_x'] = co_df[[
        'QTY_x', 'QTY_y']].apply(def_qty, axis=1)

    # (VALEC17) Deninir si un elemento es nuevo o no
    co_df['NOTE'] = co_df[[
        'AREA', 'NOTE']].apply(def_note, axis=1)

    # (VALEC17) Eliminando columnas inncesarias
    co_df.drop(['common_index', 'TAG',
               'QTY_y'], inplace=True, axis=1)

    co_df.rename(columns={'QTY_x': 'QTY'}, inplace=True)

    # (VALEC17) Guardar el archivo creado
    return co_df
