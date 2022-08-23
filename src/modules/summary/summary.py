import pandas as pd


def summary(mto_df):
    # (VALEC17) Hacer una copia del mto_df
    mto_df = mto_df.copy()

    # (VALEC17) Eliminar columnas innecesarias
    mto_df.drop(['LINE_NUM', 'SPEC'], axis=1, inplace=True)

    # (VALEC17) Convertir datos
    mto_df.convert_dtypes().dtypes

    # (VALEC17) Agrupar y sumar por cantidad peso y area
    summary_df = mto_df.groupby(['ORDER', 'TYPE', 'TYPE_CODE', 'DESCRIPTION', 'FIRST_SIZE_NUMBER',
                                 'SECOND_SIZE_NUMBER', 'SCH', 'FACE', 'RATING', 'UNITS', 'TAG', 'WEIGHT_PER_UNIT', 'NOTE'], as_index=False).agg(
        TOTAL_WEIGHT=('TOTAL_WEIGHT', sum),
        AREA=('AREA', sum),
        QTY=('QTY', sum))

    # (VALEC17) Crear el archivo summary
    return summary_df
