import pandas as pd


def summary():
    # Leer el MTO
    mto_df = pd.read_csv('./output/mto.csv')

    # Eliminar columnas innecesarias
    mto_df.drop(['LINE_NUM', 'SPEC', 'CO', 'SUPPLY'], axis=1, inplace=True)

    # Convertir datos
    mto_df.convert_dtypes().dtypes

    # Agrupar y sumar por cantidad peso y area
    mto_df = mto_df.groupby(['ORDER', 'TYPE', 'TYPE_CODE', 'DESCRIPTION', 'FIRST_SIZE_NUMBER',
                             'SECOND_SIZE_NUMBER', 'SCH', 'FACE', 'RATING', 'UNITS', 'TAG', 'WEIGHT_PER_UNIT']).agg(
        TOTAL_WEIGHT=('TOTAL_WEIGHT', sum),
        AREA=('AREA', sum),
        QTY=('QTY', sum))

    # Resetear el index
    mto_df.reset_index(drop=False)

    # Crear el archivo summary
    mto_df.to_csv('./output/summary.csv', index=True)
