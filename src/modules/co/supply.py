import pandas as pd


from src.modules.co.utils import common_index, def_area, def_catalog, def_code, def_description, def_note, def_qty, def_title, def_units


def supply():
    # Leer el MTO limpio
    co_df = pd.read_csv('./output/mto.csv')

    # Extraer únicamente las columnas necesarias
    co_df = co_df[['TYPE_CODE', 'SUPPLY_CODE', 'SUPPLY_TITLE',
                   'SUPPLY_DESCRIPTION', 'QTY']]

    # Se suman las cantidades
    co_df = co_df.groupby(['TYPE_CODE', 'SUPPLY_CODE', 'SUPPLY_TITLE',
                           'SUPPLY_DESCRIPTION'], as_index=False)[['QTY']].agg(QTY=('QTY', sum))

    # Leer el template de CO
    co_template = pd.read_csv('./src/clients/cenit/templates/co_template.csv')

    # Crear índices comunes para hacer un merge
    co_df['common_index'] = co_df[['SUPPLY_CODE', 'SUPPLY_TITLE',
                                   'SUPPLY_DESCRIPTION']].apply(common_index, axis=1)

    co_template['common_index'] = co_template[[
        'CODE', 'TITLE', 'DESCRIPTION']].apply(common_index, axis=1)

    # Hacer un merge full
    co_df = pd.merge(co_template, co_df, on='common_index', how='outer')

    # Llenar los espacios nulos
    co_df.fillna('-', inplace=True)

    # Crear la columna NOTE
    co_df['NOTE'] = '-'

    # Redefinir columnas

    # Deninir si un elemento es nuevo o no
    co_df['NOTE'] = co_df[['AREA', 'NOTE']].apply(def_note, axis=1)

    # Definir el área de mecánica y tubería
    co_df['AREA'] = co_df['AREA'].apply(def_area)

    # Definir el código
    co_df['CODE'] = co_df[['CODE', 'SUPPLY_CODE']].apply(def_code, axis=1)

    # Definir catálogo
    co_df['CATALOG'] = co_df['CATALOG'].apply(def_catalog)

    # Definir el título
    co_df['TITLE'] = co_df[['TITLE', 'SUPPLY_TITLE']].apply(def_title, axis=1)

    # Definir descrpción
    co_df['DESCRIPTION'] = co_df[['DESCRIPTION', 'SUPPLY_DESCRIPTION']].apply(
        def_description, axis=1)

    # Definir las cantidades
    co_df['QTY_x'] = co_df[['QTY_x', 'QTY_y']].apply(def_qty, axis=1)

    # Definir las unidades
    co_df['UNIT'] = co_df[['TYPE_CODE', 'UNIT']].apply(def_units, axis=1)

    # Elimuinar columnas innecesarias
    co_df.drop(['common_index', 'TYPE_CODE', 'SUPPLY_CODE',
               'SUPPLY_TITLE', 'SUPPLY_DESCRIPTION', 'QTY_y'], inplace=True, axis=1)

    # Renombrar columnas
    co_df.rename(columns={'QTY_x': 'QTY'}, inplace=True)

    # Guardar el archivo
    co_df.to_csv('./output/co.csv', index=False)
