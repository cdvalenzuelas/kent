import pandas as pd


from src.clients.cenit.co.utils import common_index, def_note, def_description


# Define la cantidad de los elementos nuevos
def def_qty(row):
    qty_x, qty_y, total_weight, unit = row

    if qty_y != '-':
        if unit == 'KG':
            return total_weight
        else:
            return qty_y

    return qty_x


def erection():
    # Leer el MTO limpio
    co_df = pd.read_csv('./output/mto.csv')

    # Extraer únicamente las columnas necesarias
    co_df = co_df[['TYPE', 'ERECTION_DESCRIPTION',
                   'TOTAL_WEIGHT', 'QTY']]

    # Se suman las cantidades
    co_df = co_df.groupby(['ERECTION_DESCRIPTION'], as_index=False)[
        ['TOTAL_WEIGHT', 'QTY']].agg(TOTAL_WEIGHT=('TOTAL_WEIGHT', sum), QTY=('QTY', sum))

    # Leer el archivo de cantidades de obra creadas
    co_template = pd.read_csv('./output/co.csv')

    # Crear índices comunes para hacer un merge
    co_df['common_index'] = co_df['ERECTION_DESCRIPTION'].apply(common_index)

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
    co_df['DESCRIPTION'] = co_df[['DESCRIPTION', 'ERECTION_DESCRIPTION']].apply(
        def_description, axis=1)

    # Definir las cantidades
    co_df['QTY_x'] = co_df[['QTY_x', 'QTY_y',
                            'TOTAL_WEIGHT', 'UNIT']].apply(def_qty, axis=1)

    # Renombrar la columna necesaria
    co_df.rename(columns={'QTY_x': 'QTY'}, inplace=True)

    # Eliminando columnas inncesarias
    co_df.drop(['common_index', 'ERECTION_DESCRIPTION',
               'TOTAL_WEIGHT', 'TOTAL_WEIGHT', 'QTY_y'], inplace=True, axis=1)

    # Guardar las cantidades de obra
    co_df.to_csv('./output/co.csv', index=False)
