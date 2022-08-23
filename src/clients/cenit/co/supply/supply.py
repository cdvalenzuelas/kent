import pandas as pd


from src.clients.cenit.co.utils.utils import common_index, def_description, def_note, def_qty, def_units


def supply(mto_df, co_df):
    # (VALEC17) Extraer únicamente las columnas necesarias
    mto_df = mto_df[['TYPE_CODE', 'SUPPLY_DESCRIPTION', 'QTY']]

    # (VALEC17) Se suman las cantidades
    mto_df = mto_df.groupby(['TYPE_CODE', 'SUPPLY_DESCRIPTION'], as_index=False)[
        ['QTY']].agg(QTY=('QTY', sum))

    # (VALEC17) Crear índices comunes para hacer un merge
    mto_df['common_index'] = mto_df['SUPPLY_DESCRIPTION'].apply(common_index)

    co_df['common_index'] = co_df['DESCRIPTION'].apply(
        common_index)

    # (VALEC17) Hacer un merge full
    co_df = pd.merge(co_df, mto_df, on='common_index', how='outer')

    # (VALEC17) Llenar los espacios nulos
    co_df.fillna('-', inplace=True)

    # (VALEC17) Crear la columna NOTE
    co_df['NOTE'] = '-'

    # (VALEC17) Redefinir columnas

    # (VALEC17) Deninir si un elemento es nuevo o no
    co_df['NOTE'] = co_df[['AREA', 'NOTE']].apply(def_note, axis=1)

    # (VALEC17) Definir descrpción
    co_df['DESCRIPTION'] = co_df[['DESCRIPTION', 'SUPPLY_DESCRIPTION']].apply(
        def_description, axis=1)

    # (VALEC17) Definir las cantidades
    co_df['QTY_x'] = co_df[['QTY_x', 'QTY_y']].apply(def_qty, axis=1)

    # (VALEC17) Definir las unidades
    co_df['UNIT'] = co_df[['TYPE_CODE', 'UNIT']].apply(def_units, axis=1)

    # (VALEC17) Elimuinar columnas innecesarias
    co_df.drop(['common_index', 'TYPE_CODE', 'SUPPLY_DESCRIPTION',
                'QTY_y'], inplace=True, axis=1)

    # (VALEC17) Renombrar columnas
    co_df.rename(columns={'QTY_x': 'QTY'}, inplace=True)

    # (VALEC17) Retornar el mto_df
    return co_df
