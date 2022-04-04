import pandas as pd
import re


# Crea una columna comun entre el mto y los bolt
def concat_bolt_index(row):
    first_size, rating, face = row

    rating = str(rating)

    rating = re.sub('[.]0', '', rating)

    return f'{first_size} {rating} {face}'


# Definir el Diámetro de los pernos
def bolts_diameter(row):
    diameter, type_code, first_size = row

    if type_code == 'BOLT':
        return diameter
    else:
        return first_size


# Definir el Diámetro de los pernos
def bolts_diameter_number(row):
    diameter, type_code, first_size_number = row

    if type_code == 'BOLT':
        return diameter
    else:
        return first_size_number


# Definir longitudes de los pernos
def bolts_length(row):
    length, type_code, second_size = row

    if type_code == 'BOLT':
        return f'{int(length)}mm'
    else:
        return second_size


# Definir longitudes de los pernos
def bolts_length_number(row):
    length, type_code, second_size_number = row

    if type_code == 'BOLT':
        return f'{int(length)}mm'
    else:
        return second_size_number


# Borrar ratings de bolts
def delete_bolts_rating(row):
    code_type, rating = row

    if code_type == 'BOLT':
        return '-'
    else:
        return rating


# Borrar face de bolts
def delete_bolts_face(row):
    code_type, face = row

    if code_type == 'BOLT':
        return '-'
    else:
        return face


# Definir el tamaño de los pernos
def bolts_weight(row):
    type_code, weight, bolt_weight = row

    if type_code == 'BOLT':
        return bolt_weight
    else:
        return weight


# Esta es la función que modifica el dataframe con respecto a los bolts
def bolts_modifier(mto_df):
    # lEER EL ARCHIVO DE PERNOS
    bolts = pd.read_csv('./src/clients/cenit/elements/bolts_kent.csv')

    # Se crean los indices para los bolts en mto y en bolts
    mto_df['BOLT_INDEX'] = mto_df[['FIRST_SIZE', 'RATING', 'FACE']].apply(
        concat_bolt_index, axis=1)

    bolts['BOLT_INDEX'] = bolts[['DIAMETER', 'RATING', 'FACE']].apply(
        concat_bolt_index, axis=1)

    # Hacer un join entre el mto y los bolts para completar el MTO
    mto_df = pd.merge(mto_df, bolts, how='left', on='BOLT_INDEX')

    # Renombrando columnas
    mto_df.rename(columns={'RATING_x': 'RATING',
                  'FACE_x': 'FACE'}, inplace=True)

    # Generar el primer tamaño de los pernos (diámetro)
    mto_df['FIRST_SIZE'] = mto_df[['BOLT_DIAMETER', 'TYPE_CODE',
                                   'FIRST_SIZE']].apply(bolts_diameter, axis=1)

    mto_df['FIRST_SIZE_NUMBER'] = mto_df[['BOLT_DIAM_NUM', 'TYPE_CODE',
                                          'FIRST_SIZE_NUMBER']].apply(bolts_diameter_number, axis=1)

    # Genear el second size de los pernos (longitud)
    mto_df['SECOND_SIZE'] = mto_df[['BOLT_LENGTH', 'TYPE_CODE',
                                   'SECOND_SIZE']].apply(bolts_length, axis=1)

    # Genear el second size de los pernos (longitud)
    mto_df['SECOND_SIZE_NUMBER'] = mto_df[['BOLT_LENGTH', 'TYPE_CODE',
                                           'SECOND_SIZE_NUMBER']].apply(bolts_length_number, axis=1)

    # Eliminar el rating de los pernos
    mto_df['RATING'] = mto_df[['TYPE_CODE', 'RATING']].apply(
        delete_bolts_rating, axis=1)

    # Eliminar el face de los pernos
    mto_df['FACE'] = mto_df[['TYPE_CODE', 'FACE']].apply(
        delete_bolts_face, axis=1)

    # Definir el peso unitario de los pernos
    mto_df['WEIGHT'] = mto_df[['TYPE_CODE', 'WEIGHT', 'BOLT_WEIGHT']].apply(
        bolts_weight, axis=1)

    # Eliminando columnas innecesarias
    mto_df.drop(['BOLT_DIAMETER', 'QUANTITY', 'BOLT_LENGTH', 'RATING_y',
                'FACE_y', 'BOLT_INDEX', 'DIAMETER', 'DIAMETER_NUMBER'], axis=1, inplace=True)

    return mto_df
