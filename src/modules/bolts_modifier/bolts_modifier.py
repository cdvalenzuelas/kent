import pandas as pd

from src.modules.bolts_modifier.bolts_utils import concat_bolt_index, bolts_diameter, bolts_diameter_number, bolts_length, bolts_length_number, bolts_weight, delete_bolts_face, delete_bolts_rating


# (VALEC17) Esta es la función que modifica el dataframe con respecto a los bolts
def bolts_modifier(mto_df):
    # (VALEC17) lEER EL ARCHIVO DE PERNOS
    bolts = pd.read_csv('./src/clients/cenit/elements/bolts_kent.csv')

    # (VALEC17) Se crean los indices para los bolts en mto y en bolts
    mto_df['BOLT_INDEX'] = mto_df[['FIRST_SIZE', 'RATING', 'FACE']].apply(
        concat_bolt_index, axis=1)

    bolts['BOLT_INDEX'] = bolts[['DIAMETER', 'RATING', 'FACE']].apply(
        concat_bolt_index, axis=1)

    # (VALEC17) Hacer un join entre el mto y los bolts para completar el MTO
    mto_df = pd.merge(mto_df, bolts, how='left', on='BOLT_INDEX')

    mto_df.fillna('-', inplace=True)

    # (VALEC17) Renombrando columnas
    mto_df.rename(columns={'RATING_x': 'RATING',
                  'FACE_x': 'FACE', 'TAG_x': 'TAG'}, inplace=True)

    # (VALEC17) Generar el primer tamaño de los pernos (diámetro)
    mto_df['FIRST_SIZE'] = mto_df[['BOLT_DIAMETER', 'TYPE_CODE',
                                   'FIRST_SIZE']].apply(bolts_diameter, axis=1)

    mto_df['FIRST_SIZE_NUMBER'] = mto_df[['BOLT_DIAM_NUM', 'TYPE_CODE',
                                          'FIRST_SIZE_NUMBER']].apply(bolts_diameter_number, axis=1)

    # (VALEC17) Genear el second size de los pernos (longitud)
    mto_df['SECOND_SIZE'] = mto_df[['BOLT_LENGTH', 'TYPE_CODE',
                                   'SECOND_SIZE']].apply(bolts_length, axis=1)

    # (VALEC17) Genear el second size de los pernos (longitud)
    mto_df['SECOND_SIZE_NUMBER'] = mto_df[['BOLT_LENGTH', 'TYPE_CODE',
                                           'SECOND_SIZE_NUMBER']].apply(bolts_length_number, axis=1)

    # (VALEC17) Eliminar el rating de los pernos
    mto_df['RATING'] = mto_df[['TYPE_CODE', 'RATING']].apply(
        delete_bolts_rating, axis=1)

    # (VALEC17) Eliminar el face de los pernos
    mto_df['FACE'] = mto_df[['TYPE_CODE', 'FACE']].apply(
        delete_bolts_face, axis=1)

    # (VALEC17) Definir el peso unitario de los pernos
    mto_df['WEIGHT'] = mto_df[['TYPE_CODE', 'WEIGHT', 'BOLT_WEIGHT']].apply(
        bolts_weight, axis=1)

    # (VALEC17) Eliminando columnas innecesarias
    mto_df.drop(['BOLT_DIAMETER', 'QUANTITY', 'BOLT_LENGTH', 'RATING_y',
                'FACE_y', 'BOLT_INDEX', 'DIAMETER', 'DIAMETER_NUMBER', 'TAG_y'], axis=1, inplace=True)

    return mto_df
