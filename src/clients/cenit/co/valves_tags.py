import imp
import pandas as pd


from src.utils.normalize_string import normalize_string
from src.clients.cenit.co.utils import common_index, def_note, def_qty


# Definir tags de válvulas
def def_valves_tags(size):
    if size < 2:
        return 'DEMARCACIÓN DE TUBERÍAS Y VÁLVULAS DIÁMETRO MENOR DE 2”'
    elif size >= 2 and size <= 6:
        return 'DEMARCACIÓN DE TUBERÍAS Y VÁLVULAS DIÁMETRO DE 2-6”'
    elif size >= 8 and size <= 14:
        return 'DEMARCACIÓN DE TUBERÍAS Y VÁLVULAS DIÁMETRO DE 8-14”'
    elif size >= 16 and size <= 30:
        return 'DEMARCACIÓN DE TUBERÍAS Y VÁLVULAS DIÁMETRO DE 16-30”'
    else:
        return 'DEMARCACIÓN DE TUBERÍAS Y VÁLVULAS DIÁMETRO MAYOR A 30”'


def valves_tags():
    # Leer el MTO limpio
    co_df = pd.read_csv('./output/mto.csv')

    # Traer únicamente las válvulas
    co_df = co_df[(co_df['TYPE'] == 'VL')]

    # Dejar únicamente las columnas necesarias
    co_df = co_df[['FIRST_SIZE_NUMBER', 'QTY']]

    # Crear la columna tag_description
    co_df['TAG'] = co_df['FIRST_SIZE_NUMBER'].apply(def_valves_tags)

    # Sumar las cantidades
    co_df = co_df.groupby(['TAG'], as_index=False)[
        ['QTY']].agg(QTY=('QTY', sum))

    # Leer el archivo de cantidades de obra creadas
    co_template = pd.read_csv('./output/co.csv')

    # Crear índice
    co_df['common_index'] = co_df['TAG'].apply(common_index)

    co_template['common_index'] = co_template['DESCRIPTION'].apply(
        common_index)

    # Hacer el merge
    co_df = pd.merge(
        co_template, co_df, on='common_index', how='outer')

    # Llenar celdas vacías
    co_df.fillna('-', inplace=True)

    # Definir las cantidades
    co_df['QTY_x'] = co_df[[
        'QTY_x', 'QTY_y']].apply(def_qty, axis=1)

    # Deninir si un elemento es nuevo o no
    co_df['NOTE'] = co_df[[
        'AREA', 'NOTE']].apply(def_note, axis=1)

    # Eliminando columnas inncesarias
    co_df.drop(['common_index', 'TAG',
               'QTY_y'], inplace=True, axis=1)

    co_df.rename(columns={'QTY_x': 'QTY'}, inplace=True)

    # Guardar el archivo creado
    co_df.to_csv('./output/co.csv', index=False)
