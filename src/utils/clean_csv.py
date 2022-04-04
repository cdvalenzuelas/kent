import pandas as pd


def clean_csv():
    # Leer archivos
    mr_df = pd.read_csv('./src/output/mr.csv')
    summary_df = pd.read_csv('./src/output/summary.csv')
    mto_df = pd.read_csv('./src/output/mto.csv')

    # Ordenar los dataframes
    summary_df.sort_values(by=['ORDER', 'TYPE_CODE', 'FIRST_SIZE_NUMBER',
                           'SECOND_SIZE_NUMBER', 'SCH', 'FACE', 'RATING', 'TAG'], inplace=True)

    mto_df.sort_values(by=['LINE_NUM', 'SPEC', 'ORDER', 'TYPE_CODE', 'FIRST_SIZE_NUMBER',
                           'SECOND_SIZE_NUMBER', 'SCH', 'FACE', 'RATING', 'TAG'], inplace=True)

    # Dejar únicamente las columnas necesarias
    mr_df = mr_df[['TAG', 'DESCRIPTION', 'FIRST_SIZE_NUMBER', 'QTY', 'UNITS']]

    summary_df = summary_df[['TYPE', 'TYPE_CODE', 'DESCRIPTION', 'FIRST_SIZE_NUMBER',
                             'SECOND_SIZE_NUMBER', 'SCH', 'FACE', 'RATING', 'QTY', 'UNITS', 'WEIGHT_PER_UNIT', 'TOTAL_WEIGHT']]

    mto_df = mto_df[['LINE_NUM', 'SPEC', 'TYPE', 'TYPE_CODE', 'DESCRIPTION', 'FIRST_SIZE_NUMBER',
                     'SECOND_SIZE_NUMBER', 'SCH', 'FACE', 'RATING', 'QTY', 'UNITS', 'WEIGHT_PER_UNIT', 'TOTAL_WEIGHT']]

    # Renombrar columnas
    mr_df.rename(
        columns={'TAG': 'CODE', 'FIRST_SIZE': 'NOMINAL_SIZE'}, inplace=True)

    # Redondeando los listados
    mto_df['TOTAL_WEIGHT'] = round(mto_df['TOTAL_WEIGHT'], 4)
    mto_df['WEIGHT_PER_UNIT'] = round(mto_df['WEIGHT_PER_UNIT'], 4)

    summary_df['TOTAL_WEIGHT'] = round(summary_df['TOTAL_WEIGHT'], 4)
    summary_df['WEIGHT_PER_UNIT'] = round(summary_df['WEIGHT_PER_UNIT'], 4)

    # Crear el archivos
    mr_df.to_csv('./src/output/mr.csv', index=False)
    summary_df.to_csv('./src/output/summary.csv', index=False)
    mto_df.to_csv('./src/output/mto.csv', index=False)
