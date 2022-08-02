import pandas as pd
import re
import os

from src.modules.diagnostic.compare.compare import compare


# Crea una columna comun entre el mto y los bolt
def concat_bolt_index(row):
    first_size, rating, face = row

    rating = str(rating)

    rating = re.sub('[.]0', '', rating)

    return f'{first_size} {rating} {face}'


def diagnostic(mto_df):
    # Crear un índice artificial
    index = pd.DataFrame({'INDEX': list(range(1, mto_df.shape[0] + 1))})

    # lEER EL ARCHIVO DE PERNOS
    bolts = pd.read_csv('./src/clients/cenit/elements/bolts_kent.csv')

    # Unir el indice y el mto en un dataframe
    mto_df = pd.concat([index, mto_df], axis=1)

    # Se crean los indices para los bolts en mto y en bolts
    mto_df['BOLT_INDEX'] = mto_df[['FIRST_SIZE', 'RATING', 'FACE']].apply(
        concat_bolt_index, axis=1)

    bolts = bolts[bolts['RATING'].notnull() & bolts['FACE'].notnull()]

    bolts['BOLT_INDEX'] = bolts[['DIAMETER', 'RATING', 'FACE']].apply(
        concat_bolt_index, axis=1)

    # Hacer un joint con la tabla pernos
    mto_df = pd.merge(mto_df, bolts, how='left', on='BOLT_INDEX')

    mto_df.fillna('-', inplace=True)

    mto_df = mto_df[['INDEX', 'LINE_NUM', 'TYPE_CODE', 'SHORT_DESC', 'SHORT_DESCRIPTION', 'WEIGHT_x',
                    'WEIGHT_y', 'LENGTH', 'BOLT_LENGTH', 'QTY', 'BOLT_WEIGHT', 'FIRST_SIZE', 'BOLT_DIAMETER', 'SECOND_SIZE', 'RATING_x', 'SCH', 'TAG_y']]

    # Crear un diccionario con las diferencias o diagnóstico
    diagnostic_dict = {
        'index': [],
        'description_spec': [],
        'description_piping': [],
        'weight_spec': [],
        'weight_piping': [],
        'bolt_length_spec': [],
        'bolt_length_piping': [],
        'sch_piping': [],
        'rating_piping': []
    }

    mto_df['INDEX'] = mto_df[['INDEX', 'LINE_NUM', 'TYPE_CODE', 'SHORT_DESC', 'SHORT_DESCRIPTION', 'WEIGHT_x',
                              'WEIGHT_y', 'LENGTH', 'BOLT_LENGTH', 'QTY', 'BOLT_WEIGHT', 'FIRST_SIZE', 'BOLT_DIAMETER', 'SECOND_SIZE', 'RATING_x', 'SCH', 'TAG_y']].apply(compare, diagnostic_dict=diagnostic_dict, axis=1)

    diagnostic_length = 0

    with open('./output/diagnostic.txt', mode='r') as f:
        diagnostic_length = len(f.readlines())

    if diagnostic_length == 0:
        os.remove('./output/diagnostic.txt')
