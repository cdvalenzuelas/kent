import pandas as pd


# (VALEC17) Función para hacer un merge
def common_index(row):
    line, spec, type_code, first_size, second_size, tag = row
    return f'{line} {spec} {type_code} {tag} {first_size} {second_size}'


# (VALEC17) Change data
def change_data(row):
    data_mto, data_pid = row

    # (VALEC17) Si el dato existe el MTO dejarlo
    if str(data_mto) != 'nan':
        return data_mto
    # (VALEC17) En caso contrario dejar el del P&ID
    else:
        return data_pid


def elements_difference(mto_df, pid_df):
    # (VALEC17) Hacer una copia de los dataframes
    mto_df = mto_df.copy()
    pid_df = pid_df.copy()

    # (VALEC17) Sacar únicamente elementos importantes
    mto_df = mto_df[~mto_df['TYPE_CODE'].isin([
        'BE', 'PE', 'TE', '45L', '90L', 'CPL'])]

    # (VALEC17) Traer únicamente los elementos importantes
    pid_df = pid_df[pid_df['QTY'] != 0]

    # (VALEC17) Crear un índice común entre el bom y el p&id
    mto_df['common_index'] = mto_df[['LINE_NUM', 'SPEC', 'TYPE_CODE',
                                    'FIRST_SIZE_NUMBER', 'SECOND_SIZE_NUMBER', 'TAG']].apply(common_index, axis=1)

    pid_df['common_index'] = pid_df[['LINE_NUM', 'SPEC', 'TYPE_CODE',
                                    'FIRST_SIZE_NUMBER', 'SECOND_SIZE_NUMBER', 'TAG']].apply(common_index, axis=1)

    # (VALEC17) Hacer el Merge
    merge_df = pd.merge(mto_df, pid_df, how='outer', on='common_index')

    # (VALEC17) Eliminar el common_index
    merge_df.drop(['common_index'], inplace=True, axis=1)

    # (VALEC17) Rellenar los datos necesario
    merge_df['LINE_NUM_x'] = merge_df[['LINE_NUM_x',
                                       'LINE_NUM_y']].apply(change_data, axis=1)

    merge_df['SPEC_x'] = merge_df[['SPEC_x',
                                   'SPEC_y']].apply(change_data, axis=1)

    merge_df['TYPE_CODE_x'] = merge_df[['TYPE_CODE_x',
                                        'TYPE_CODE_y']].apply(change_data, axis=1)

    merge_df['FIRST_SIZE_NUMBER_x'] = merge_df[['FIRST_SIZE_NUMBER_x',
                                                'FIRST_SIZE_NUMBER_y']].apply(change_data, axis=1)

    merge_df['SECOND_SIZE_NUMBER_x'] = merge_df[['SECOND_SIZE_NUMBER_x',
                                                 'SECOND_SIZE_NUMBER_y']].apply(change_data, axis=1)

    merge_df['TAG_x'] = merge_df[['TAG_x',
                                  'TAG_y']].apply(change_data, axis=1)

    # (VALEC17) Eliminar columnas innecesrias
    merge_df.drop(columns=['SPEC_y', 'TYPE_CODE_y', 'FIRST_SIZE_NUMBER_y', 'SECOND_SIZE_NUMBER_y', 'ORDER', 'TYPE',
                  'CSO', 'CSC', 'TAG_y', 'AREA', 'WEIGHT_PER_UNIT', 'LINE_NUM_y', 'NO_LOCKING_DEVICE', 'UNITS', 'SCH', 'FACE', 'TOTAL_WEIGHT', 'FIRST_SIZE', 'SECOND_SIZE', 'RATING'], inplace=True)

    # (VALEC17) Renombrar columnas
    merge_df.rename(columns={'LINE_NUM_x': 'LINE_NUM',
                    'SPEC_x': 'SPEC', 'TYPE_CODE_x': 'TYPE_CODE', 'QTY_x': 'QTY_MTO', 'QTY_y': 'QTY_P&ID', 'TAG_x': 'TAG', 'SECOND_SIZE_NUMBER_x': 'SECOND_SIZE_NUMBER', 'FIRST_SIZE_NUMBER_x': 'FIRST_SIZE_NUMBER'}, inplace=True)

    # (VALEC17) Rellenar los nulos con ceros
    merge_df['QTY_P&ID'].fillna(0, inplace=True)

    merge_df['QTY_MTO'].fillna(0, inplace=True)

    # (VALEC17) Dejar únicamente los elementos que tienen diferencias en válvulas
    merge_df = merge_df[merge_df['QTY_P&ID'] != merge_df['QTY_MTO']]

    # (VALEC17) Ordenar el df
    merge_df.sort_values(by=['LINE_NUM', 'SPEC', 'TYPE_CODE'], inplace=True)

    # (VALEC17) Generar el archivo
    merge_df.to_csv('./diacnostic/4.difference_elements.csv', index=False)
