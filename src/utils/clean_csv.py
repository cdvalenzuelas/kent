import pandas as pd


# Reemplaza puntos por comas
def replace_dot_by_comma(data):
    if type(data) == float or type(data) == int:
        if data % 1 == 0:
            data = str(int(data))
        else:
            data = str(data)

    data = data.replace('.', ',')

    return data


def clean_csv():
    # Leer archivos
    mr_df = pd.read_csv('./output/mr.csv')
    summary_df = pd.read_csv('./output/summary.csv')
    mto_df = pd.read_csv('./output/mto.csv')
    co_df = pd.read_csv('./output/co.csv')

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

    # Cambiar puntos por comas en todos los archivos de salida
    mto_df['FIRST_SIZE_NUMBER'] = mto_df['FIRST_SIZE_NUMBER'].apply(
        replace_dot_by_comma)
    mto_df['SECOND_SIZE_NUMBER'] = mto_df['SECOND_SIZE_NUMBER'].apply(
        replace_dot_by_comma)
    mto_df['WEIGHT_PER_UNIT'] = mto_df['WEIGHT_PER_UNIT'].apply(
        replace_dot_by_comma)
    mto_df['TOTAL_WEIGHT'] = mto_df['TOTAL_WEIGHT'].apply(replace_dot_by_comma)

    summary_df['FIRST_SIZE_NUMBER'] = summary_df['FIRST_SIZE_NUMBER'].apply(
        replace_dot_by_comma)
    summary_df['SECOND_SIZE_NUMBER'] = summary_df['SECOND_SIZE_NUMBER'].apply(
        replace_dot_by_comma)
    summary_df['WEIGHT_PER_UNIT'] = summary_df['WEIGHT_PER_UNIT'].apply(
        replace_dot_by_comma)
    summary_df['TOTAL_WEIGHT'] = summary_df['TOTAL_WEIGHT'].apply(
        replace_dot_by_comma)

    co_df['QTY'] = co_df['QTY'].apply(
        replace_dot_by_comma)

    # Poner una columna de items (numeración en cada documento)
    item = pd.DataFrame({'ITEM': list(range(1, mr_df.shape[0] + 1))})
    mr_df = pd.concat([item, mr_df], axis=1)

    item = pd.DataFrame({'ITEM': list(range(1, summary_df.shape[0] + 1))})
    summary_df = pd.concat([item, summary_df], axis=1)

    item = pd.DataFrame({'ITEM': list(range(1, mto_df.shape[0] + 1))})
    mto_df = pd.concat([item, mto_df], axis=1)

    # Crear el archivos
    mr_df.to_csv('./output/mr.csv', index=False)
    mr_df.to_excel('./output/mr.xlsx', index=False)

    summary_df.to_csv('./output/summary.csv', index=False)
    summary_df.to_excel('./output/summary.xlsx', index=False)

    mto_df.to_csv('./output/mto.csv', index=False)
    mto_df.to_excel('./output/mto.xlsx', index=False)

    co_df.to_csv('./output/co.csv', index=False)
    co_df.to_excel('./output/co.xlsx', index=False)
