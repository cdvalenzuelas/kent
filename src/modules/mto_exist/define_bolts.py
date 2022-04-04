import pandas as pd


# Crear una función para generar el bolt_index desde el archivo de Bolts
def create_bolt_index_1(row):
    first_size, second_size = row

    second_size = int(second_size)

    return f'{first_size} {second_size}mm'


# Crear una función para generar el bolt_index desde el MTO
def create_bolt_index_2(row):
    type_code, first_size, second_size = row

    if type_code == 'BOLT':
        return f'{first_size} {second_size}'
    else:
        return '-'


# Definir el first_size_number de los pernos
def bolt_first_size_number(row):
    type_code, first_size_number, bolt_diameter_number = row

    if type_code == 'BOLT':
        return bolt_diameter_number
    else:
        return first_size_number


# Definir el second_size_number de los pernos
def bolt_second_size_number(row):
    type_code, second_size_number, bolt_length = row

    if type_code == 'BOLT':
        return bolt_length
    else:
        return second_size_number


# Definir el weight de los pernos
def bolts_weight(row):
    type_code, weight, bolt_weight = row

    if type_code == 'BOLT':
        return bolt_weight
    else:
        return weight


# Poner SCH_y de los bolts
def bolts_sch_y(row):
    type_code, sch_y = row

    if type_code == 'BOLT':
        return '-'
    else:
        return sch_y


# Poner FACE_y de los bolts
def bolts_face_y(row):
    type_code, face_y = row

    if type_code == 'BOLT':
        return '-'
    else:
        return face_y


# Poner RATING_y de los bolts
def bolts_rating_y(row):
    type_code, rating_y = row

    if type_code == 'BOLT':
        return '-'
    else:
        return rating_y


# Poner TYPE_y de los bolts
def bolts_type_y(row):
    type_code, type_y = row

    if type_code == 'BOLT':
        return 'BL'
    else:
        return type_y


# Poner SHORT_DESCRIPTION de los bolts
def bolts_short_description(row):
    type_code, short_description = row

    if type_code == 'BOLT':
        return 'STUD BOLTS W/2 HVY HEX NUTS, CS, A193 Gr.B7/A194 Gr.2H, ASME B18.2.1/B18.2.2'
    else:
        return short_description


# Regresa el mto con los bolts entregados
def define_bolts(mto_df, piping_class):
    # Leer el archivo de bolts
    bolts_df_1 = pd.read_csv('./src/clients/cenit/elements/bolts_kent.csv')

    # Eliminar las columnas innecesarias
    bolts_df_1.drop(['RATING', 'DIAMETER', 'DIAMETER_NUMBER', 'FACE',
                    'QUANTITY'], inplace=True, axis=1)

    # Eliminar los diámetros nulos
    bolts_df_1 = bolts_df_1[bolts_df_1['BOLT_DIAMETER'].notnull()]

    # Eliminar pernos repetidos en el archivo de bolts
    bolts_df_1.drop_duplicates(
        ['BOLT_DIAMETER', 'BOLT_LENGTH'], keep='last', inplace=True)

    # Crear un índice en común
    bolts_df_1['bolt_index'] = bolts_df_1[['BOLT_DIAMETER',
                                           'BOLT_LENGTH']].apply(create_bolt_index_1, axis=1)

    # Crear un índice en común
    mto_df['bolt_index'] = mto_df[['TYPE_CODE', 'FIRST_SIZE',
                                   'SECOND_SIZE']].apply(create_bolt_index_2, axis=1)

    # Hacer un join entre el MTO y los bolts
    mto_df = pd.merge(mto_df, bolts_df_1,
                      how='left', on='bolt_index')

    # Definir el first_size_number de los pernos
    mto_df['FIRST_SIZE_NUMBER'] = mto_df[[
        'TYPE_CODE', 'FIRST_SIZE_NUMBER', 'BOLT_DIAM_NUM']].apply(bolt_first_size_number, axis=1)

    # Definir el second_size_number de los pernos
    mto_df['SECOND_SIZE_NUMBER'] = mto_df[[
        'TYPE_CODE', 'SECOND_SIZE_NUMBER', 'BOLT_LENGTH']].apply(bolt_second_size_number, axis=1)

    # Definir el weight de los pernos
    mto_df['WEIGHT'] = mto_df[[
        'TYPE_CODE', 'WEIGHT', 'BOLT_WEIGHT']].apply(bolts_weight, axis=1)

    # Eliminar columnas innecesarias luego del merge
    mto_df.drop(['bolt_index', 'BOLT_DIAMETER', 'BOLT_DIAM_NUM', 'BOLT_LENGTH',
                 'BOLT_WEIGHT'], inplace=True, axis=1)

    # Poner SCH_y de los bolts
    mto_df['SCH_y'] = mto_df[['TYPE_CODE', 'SCH_y']].apply(bolts_sch_y, axis=1)

    # Poner FACE_y de los bolts
    mto_df['FACE_y'] = mto_df[['TYPE_CODE', 'FACE_y']].apply(
        bolts_face_y, axis=1)

    # Poner RATING_y de los bolts
    mto_df['RATING_y'] = mto_df[['TYPE_CODE', 'RATING_y']].apply(
        bolts_rating_y, axis=1)

    # Poner TYPE_y de los bolts
    mto_df['TYPE_y'] = mto_df[['TYPE_CODE', 'TYPE_y']].apply(
        bolts_type_y, axis=1)

    # Poner SHORT_DESCRIPTION de los bolts
    mto_df['SHORT_DESCRIPTION'] = mto_df[['TYPE_CODE', 'SHORT_DESCRIPTION']].apply(
        bolts_short_description, axis=1)

    return mto_df
