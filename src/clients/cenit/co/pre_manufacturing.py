import pandas as pd


from src.clients.cenit.co.utils import common_index, def_note, def_description, def_qty


def pre_manufacturing():
    # Leer el MTO limpio
    co_df = pd.read_csv('./output/mto.csv')

    # Extraer únicamente las columnas necesarias
    co_df = co_df[['TYPE', 'MANUFACTURING_DESCRIPTION', 'TOTAL_WEIGHT']]

    # Eliminar válvulas y elementos que no tienen prefabricación, como bolts, gaskets,
    co_df = co_df[(co_df['TYPE'] != 'VL') & (
        co_df['MANUFACTURING_DESCRIPTION'] != '-')]

    # Se suman los pesos
    co_df = co_df.groupby(['MANUFACTURING_DESCRIPTION'], as_index=False)[
        ['TOTAL_WEIGHT']].agg(TOTAL_WEIGHT=('TOTAL_WEIGHT', sum))

    # Leer el archivo de cantidades de obra creadas
    co_template = pd.read_csv('./output/co.csv')

    # Crear índices comunes para hacer un merge
    co_df['common_index'] = co_df['MANUFACTURING_DESCRIPTION'].apply(
        common_index)

    co_template['common_index'] = co_template['DESCRIPTION'].apply(
        common_index)

    # Hacer un merge full
    co_df = pd.merge(co_template, co_df, on='common_index', how='outer')

    # Llenar los espacios nulos
    co_df.fillna('-', inplace=True)

    # Redefinir columnas

    # Deninir si un elemento es nuevo o no
    co_df['NOTE'] = co_df[['AREA', 'NOTE']].apply(def_note, axis=1)

    # Definir descrpción
    co_df['DESCRIPTION'] = co_df[['DESCRIPTION', 'MANUFACTURING_DESCRIPTION']].apply(
        def_description, axis=1)

    # Definir las cantidades
    co_df['QTY'] = co_df[['QTY', 'TOTAL_WEIGHT']].apply(def_qty, axis=1)

    # Eliminando columnas inncesarias
    co_df.drop(['common_index', 'MANUFACTURING_DESCRIPTION',
               'TOTAL_WEIGHT'], inplace=True, axis=1)

    # Guardar las cantidades de obra
    co_df.to_csv('./output/co.csv', index=False)
