import pandas as pd


def summary(mto_df):
    # Hacer una copia del mto_df
    mto_df = mto_df.copy()

    # Eliminar columnas innecesarias
    mto_df.drop(['LINE_NUM', 'SPEC'], axis=1, inplace=True)

    # Convertir datos
    mto_df.convert_dtypes().dtypes

    # Agrupar y sumar por cantidad peso y area
    summary_df = mto_df.groupby(['ORDER', 'TYPE', 'TYPE_CODE', 'DESCRIPTION', 'FIRST_SIZE_NUMBER',
                                 'SECOND_SIZE_NUMBER', 'SCH', 'FACE', 'RATING', 'UNITS', 'TAG', 'WEIGHT_PER_UNIT', 'NOTE'], as_index=False).agg(
        TOTAL_WEIGHT=('TOTAL_WEIGHT', sum),
        AREA=('AREA', sum),
        QTY=('QTY', sum))

    # Crear el archivo summary
    return summary_df
