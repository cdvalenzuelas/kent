import pandas as pd


def bolts_qty(pid_df, piping_class):
    # (VALEC17) Hacer una copia del P&ID y piping_class
    pid_df = pid_df.copy()
    piping_class = piping_class.copy()

    # (VALEC17) Dejar únicamente los bolts del piping class
    piping_class = piping_class[(piping_class['TYPE_CODE'] == 'BOLT')]

    # (VALEC17) Dejar únicamente las columnas necesarias
    piping_class = piping_class[[
        'TYPE_CODE', 'SPEC', 'FIRST_SIZE_NUMBER', 'RATING', 'FACE']]

    # (VALEC17) Leer el archivo de pernos
    bols_df = pd.read_csv('./src/clients/cenit/elements/bolts_kent.csv')

    # (VALEC17) Colocarle el type code al dataframe de pernos
    bols_df['TYPE_CODE'] = 'BOLT'

    # (VALEC17) Crear un indice común
    piping_class['common_index'] = piping_class[['TYPE_CODE', 'FIRST_SIZE_NUMBER',
                                                'SPEC']].apply(lambda x: f"{x['TYPE_CODE']} {x['FIRST_SIZE_NUMBER']} {x['SPEC']}", axis=1)

    pid_df['common_index'] = pid_df[['TYPE_CODE', 'FIRST_SIZE_NUMBER',
                                     'SPEC']].apply(lambda x: f"{x['TYPE_CODE']} {x['FIRST_SIZE_NUMBER']} {x['SPEC']}", axis=1)

    # (VALEC17) Hacer el merge
    pid_df = pd.merge(pid_df, piping_class, how='left', on='common_index')

    # (VALEC17) Eliminar columnas innecesarias
    pid_df.drop(columns=['common_index',
                'TYPE_CODE_y', 'SPEC_y', 'FIRST_SIZE_NUMBER_y'], inplace=True)

    # (VALEC17) Renombrar columnas
    pid_df.rename(columns={'SPEC_x': 'SPEC',
                  'TYPE_CODE_x': 'TYPE_CODE', 'FIRST_SIZE_NUMBER_x': 'FIRST_SIZE_NUMBER'}, inplace=True)

    # (VALEC17) Cuadrar un nuevo common_index para unirlo con el archivo de pernos
    pid_df['common_index'] = pid_df[['TYPE_CODE', 'FIRST_SIZE_NUMBER',
                                     'RATING', 'TAG', 'FACE']].apply(lambda x: f"{x['TYPE_CODE']} {x['FIRST_SIZE_NUMBER']} {x['RATING']} {x['TAG']} {x['FACE']}", axis=1)

    bols_df['common_index'] = bols_df[['TYPE_CODE', 'DIAMETER_NUMBER',
                                       'RATING', 'TAG', 'FACE']].apply(lambda x: f"{x['TYPE_CODE']} {x['DIAMETER_NUMBER']} {x['RATING']} {x['TAG']} {x['FACE']}", axis=1)

    # (VALEC17) Hacer el merge
    pid_df = pd.merge(pid_df, bols_df, how='left', on='common_index')

    # (VALEC17) Detectar la verdadera cantidad de los pernos
    pid_df['NO_LOCKING_DEVICE'] = pid_df[['NO_LOCKING_DEVICE', 'QUANTITY', 'TYPE_CODE_x']].apply(
        lambda x: x['NO_LOCKING_DEVICE'] * x['QUANTITY'] if x['TYPE_CODE_x'] == 'BOLT' else x['NO_LOCKING_DEVICE'], axis=1)

    # (VALEC17) Redefinir la longitud y diámetro de pernos
    pid_df['FIRST_SIZE_NUMBER'] = pid_df[['TYPE_CODE_x', 'FIRST_SIZE_NUMBER', 'BOLT_DIAM_NUM']].apply(
        lambda x: x['BOLT_DIAM_NUM'] if x['TYPE_CODE_x'] == 'BOLT' else x['FIRST_SIZE_NUMBER'], axis=1)

    pid_df['SECOND_SIZE_NUMBER'] = pid_df[['TYPE_CODE_x', 'SECOND_SIZE_NUMBER', 'BOLT_LENGTH']].apply(
        lambda x: f"{int(x['BOLT_LENGTH'])}mm" if x['TYPE_CODE_x'] == 'BOLT' else x['SECOND_SIZE_NUMBER'], axis=1)

    # (VALEC17) Eliminar columnas innecesarias
    pid_df.drop(columns=['common_index', 'RATING_y', 'DIAMETER', 'DIAMETER_NUMBER', 'FACE_y',
                'BOLT_DIAMETER', 'BOLT_WEIGHT', 'TAG_y', 'TYPE_CODE_y', 'QUANTITY', 'RATING_x', 'FACE_x', 'BOLT_DIAMETER'], inplace=True)

    # (VALEC17) Renombrar columnas
    pid_df.rename(columns={'TYPE_CODE_x': 'TYPE_CODE',
                  'TAG_x': 'TAG', 'FIRST_SIZE_NUMBER_x': 'FIRST_SIZE_NUMBER'}, inplace=True)

    return pid_df
