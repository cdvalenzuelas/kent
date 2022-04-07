import pandas as pd


from src.modules.co.utils import common_index, def_note, def_area, def_code, def_catalog, def_title, def_description, def_qty


def valves_hidrostatic_test():
    # Leer el MTO limpio
    co_df = pd.read_csv('./output/mto.csv')

    # Extraer únicamente las columnas necesarias
    co_df = co_df[['TYPE', 'TYPE_CODE', 'MANUFACTURING_CODE', 'MANUFACTURING_TITLE',
                   'MANUFACTURING_DESCRIPTION', 'QTY']]

    # Eliminar válvulas y elementos que no tienen prefabricación, como bolts, gaskets,
    co_df = co_df[(co_df['TYPE'] == 'VL')]

    # Se suman las cantidades
    co_df = co_df.groupby(['MANUFACTURING_CODE', 'MANUFACTURING_TITLE',
                           'MANUFACTURING_DESCRIPTION'], as_index=False)[['QTY']].agg(QTY=('QTY', sum))

    # Leer el archivo de cantidades de obra creadas
    co_template = pd.read_csv('./output/co.csv')

    # Crear índices comunes para hacer un merge
    co_df['common_index'] = co_df[['MANUFACTURING_CODE', 'MANUFACTURING_TITLE',
                                   'MANUFACTURING_DESCRIPTION']].apply(common_index, axis=1)

    co_template['common_index'] = co_template[[
        'CODE', 'TITLE', 'DESCRIPTION']].apply(common_index, axis=1)

    # Hacer un merge full
    co_df = pd.merge(co_template, co_df, on='common_index', how='outer')

    # Llenar los espacios nulos
    co_df.fillna('-', inplace=True)

    # Redefinir columnas

    # Deninir si un elemento es nuevo o no
    co_df['NOTE'] = co_df[['AREA', 'NOTE']].apply(def_note, axis=1)

    # Definir el área de mecánica y tubería
    co_df['AREA'] = co_df['AREA'].apply(def_area)

    # Definir el código
    co_df['CODE'] = co_df[['CODE', 'MANUFACTURING_CODE']].apply(
        def_code, axis=1)

    # Definir catálogo
    co_df['CATALOG'] = co_df['CATALOG'].apply(def_catalog)

    # Definir el título
    co_df['TITLE'] = co_df[['TITLE', 'MANUFACTURING_TITLE']].apply(
        def_title, axis=1)

    # Definir descrpción
    co_df['DESCRIPTION'] = co_df[['DESCRIPTION', 'MANUFACTURING_DESCRIPTION']].apply(
        def_description, axis=1)

    # Definir las cantidades
    co_df['QTY_x'] = co_df[['QTY_x', 'QTY_y']].apply(def_qty, axis=1)

    # Eliminando columnas inncesarias
    co_df.drop(['common_index', 'MANUFACTURING_CODE', 'MANUFACTURING_TITLE',
                'MANUFACTURING_DESCRIPTION', 'QTY_y'], inplace=True, axis=1)

    # Renombrar columnas
    co_df.rename(columns={'QTY_x': 'QTY'}, inplace=True)

    # Guardar las cantidades de obra
    co_df.to_csv('./output/co.csv', index=False)
