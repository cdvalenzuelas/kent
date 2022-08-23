import pandas as pd


def common_index(row):
    line, spec, type_code, size, tag = row

    return f'{line} {spec} {type_code} {size} {tag}'


# (VALEC17) Definir las notas
def note(line_y):
    if str(line_y) != 'nan':
        return 'delete'
    else:
        return '-'


def locking_device(mto_df, pid_df):
    # (VALEC17) Eliminar las filas que no tienen válvulas o que las válvulas que no se hayan encontrado
    pid_df = pid_df[(pid_df['QTY'] > 0) & (pid_df['TAG'] != 'error')]

    # (VALEC17) Eliminar las filas que no tienen cantidad o que no tienen locking device (no son relevantes para el análisis)
    pid_df_locking_device_only = pid_df[(pid_df['QTY'] > 0) & (
        pid_df['QTY'] > pid_df['NO_LOCKING_DEVICE'])]

    # (VALEC17) Se crea la columna Note en el MTO
    mto_df['NOTE'] = '-'

    if pid_df_locking_device_only.shape[0] == 0:
        return mto_df.copy()

    pid_df_locking_device_only = pid_df_locking_device_only.copy()

    # (VALEC17) Crear índices comunes entre el MTO y el P&ID
    mto_df['common_index'] = mto_df[['LINE_NUM', 'SPEC', 'TYPE_CODE',
                                     'FIRST_SIZE_NUMBER', 'TAG']].apply(common_index, axis=1)

    pid_df_locking_device_only['common_index'] = pid_df_locking_device_only[['LINE_NUM', 'SPEC', 'TYPE_CODE',
                                                                             'FIRST_SIZE_NUMBER', 'TAG']].apply(common_index, axis=1)

    # (VALEC17) Hacer un merge entre MTO y P&ID
    mto_df = pd.merge(mto_df, pid_df_locking_device_only,
                      how='left', on='common_index')

    # (VALEC17) Crear la nolumna NOTE del MTO
    mto_df['NOTE'] = mto_df['LINE_NUM_y'].apply(note)

    # (VALEC17) Eliminar columnas innecesarias
    mto_df.drop(columns=['LINE_NUM_y', 'SPEC_y',
                'TYPE_CODE_y', 'FIRST_SIZE_NUMBER_y', 'RATING_y', 'QTY_y', 'TAG_y', 'common_index'], inplace=True)

    # (VALEC17) Renombrar columnas
    mto_df.rename(columns={'LINE_NUM_x': 'LINE_NUM',
                  'SPEC_x': 'SPEC', 'TYPE_CODE_x': 'TYPE_CODE', 'FIRST_SIZE_NUMBER_x': 'FIRST_SIZE_NUMBER', 'RATING_x': 'RATING', 'TAG_x': 'TAG', 'QTY_x': 'QTY'}, inplace=True)

    # (VALEC17) Iterar todas las filas en busca de las válvulas que tienen locking device
    for index, row in mto_df.iterrows():
        if row['NOTE'] == 'delete':
            row_dict = row

            # (VALEC17) Extraer las cantidades de CSO, CSC y NO_LOCKING_DEVICE
            cso = row_dict['CSO']
            csc = row_dict['CSC']
            no_locking_device = row_dict['NO_LOCKING_DEVICE']

            # (VALEC17) Creando los diccionarios necesrio para crear los dataframes que se anezarán
            if cso:
                cso_locking_device = row_dict.copy()
                cso_locking_device['QTY'] = cso
                cso_locking_device['NOTE'] = 'CSO'
                cso_locking_device['TOTAL_WEIGHT'] = cso_locking_device['WEIGHT_PER_UNIT'] * cso

                # (VALEC17) Combinar df
                mto_df = pd.concat(
                    [mto_df, pd.DataFrame(cso_locking_device).T], axis=0)

            if csc:
                csc_locking_device = row_dict.copy()
                csc_locking_device['QTY'] = csc
                csc_locking_device['NOTE'] = 'CSC'
                csc_locking_device['TOTAL_WEIGHT'] = csc_locking_device['WEIGHT_PER_UNIT'] * csc

                # (VALEC17) Combinar df
                mto_df = pd.concat(
                    [mto_df, pd.DataFrame(csc_locking_device).T], axis=0)

            if no_locking_device:
                no_locking_device_dict = row_dict.copy()
                no_locking_device_dict['QTY'] = no_locking_device
                no_locking_device_dict['NOTE'] = '-'
                no_locking_device_dict['TOTAL_WEIGHT'] = no_locking_device_dict['WEIGHT_PER_UNIT'] * no_locking_device

                # (VALEC17) Combinar df
                mto_df = pd.concat(
                    [mto_df, pd.DataFrame(no_locking_device_dict).T], axis=0)

    # (VALEC17) Eliminar columnas innecesarias
    mto_df.drop(columns=['CSO', 'CSC', 'NO_LOCKING_DEVICE'], inplace=True)

    # (VALEC17) Eliminar las columnas a las que ya se les ha hecho un análisis de locking device
    mto_df = mto_df[(mto_df['NOTE'] != 'delete')]

    # (VALEC17) Reconstruir el index
    mto_df.reset_index(inplace=True)

    return mto_df.copy()
