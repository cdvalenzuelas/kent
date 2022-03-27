import pandas as pd
import re


from src.mto_exist.define_tag import define_tag
from src.mto_exist.define_bolts import define_bolts


# Crea una columna comun entre el piping class y el bom
def concat_colums(row):
    spec, type_code, first_size, second_size, tag = row
    return f'{spec} {type_code} {first_size} {second_size} {tag}'


# Modificar el segundo tamaño
def modify_size(second_size):
    size = re.sub(' mm', 'mm', str(second_size))
    size = re.sub('"', '', str(size))
    size = re.sub('[\s]', '-', str(size))
    size = re.sub(',', '.', str(size))
    size = re.sub(' ', '-', str(size))
    size += '"'
    size = re.sub('mm"', 'mm', str(size))
    size = re.sub('-"', '-', str(size))

    if size == '0.5"':
        size = '1/2"'
    elif size == '0.625"':
        size = '5/8"'
    elif size == '0.75"':
        size = '3/4"'
    elif size == '0.875"':
        size = '7/8"'
    elif size == '1.125"':
        size = '1-1/8"'
    elif size == '1.25"':
        size = '1-1/4"'
    elif size == '1.375"':
        size = '1-3/8"'
    elif size == '1.625"':
        size = '1-5/8"'
    elif size == '1.5"':
        size = '1-1/2"'
    elif size == '1.875"':
        size = '1-7/8"'
    elif size == '2.25"':
        size = '2-1/4"'
    elif size == '2.5"':
        size = '2-1/2"'
    elif size == '2.75"':
        size = '2-3/4"'
    elif size == '3.5"':
        size = '3-1/2"'

    return size


# Carbiar BW por BE
def change_bw_by_be(description):
    description = re.sub(' BW,', ' BE,', description)

    return description


def mto_cleaner():
    # Leer el MTO
    mto_df = pd.read_csv('mto.csv')

    # Rellenar espacios vacío
    mto_df.fillna('-', inplace=True)

    # Carbiar BW por BE
    mto_df['DESCRIPTION'] = mto_df['DESCRIPTION'].apply(change_bw_by_be)

    # Renombrando el first size del MTO entyregado
    mto_df['FIRST_SIZE'] = mto_df['FIRST_SIZE'].apply(modify_size)

    # Renombrando el second size del MTO entregado
    mto_df['SECOND_SIZE'] = mto_df['SECOND_SIZE'].apply(modify_size)

    # Extraer el piping class
    CS2SA1 = pd.read_csv('./CENIT/PIPING_CLASS/CS2SA1.csv')
    CS3SA1 = pd.read_csv('./CENIT/PIPING_CLASS/CS3SA1.csv')
    CS5SA1 = pd.read_csv('./CENIT/PIPING_CLASS/CS5SA1.csv')
    CS6SA1 = pd.read_csv('./CENIT/PIPING_CLASS/CS6SA1.csv')
    CS1SC2 = pd.read_csv('./CENIT/PIPING_CLASS/CS1SC2.csv')

    piping_class = pd.concat([CS2SA1, CS3SA1, CS5SA1, CS6SA1, CS1SC2])

    # Carbiar BW por BE
    piping_class['SHORT_DESCRIPTION'] = piping_class['SHORT_DESCRIPTION'].apply(
        change_bw_by_be)

    # Se buscar los tags
    mto_df = define_tag(mto_df, piping_class)

    # Se crean los índices del BOM y del piping class
    mto_df['common_index'] = mto_df[['SPEC', 'TYPE_CODE', 'FIRST_SIZE',
                                     'SECOND_SIZE', 'TAG']].apply(concat_colums, axis=1)

    piping_class['common_index'] = piping_class[['SPEC', 'TYPE_CODE', 'FIRST_SIZE',
                                                 'SECOND_SIZE', 'TAG']].apply(concat_colums, axis=1)

    # Hacer un join entre el bom y el piping class para generar el mto
    mto_df = pd.merge(mto_df, piping_class, how='left', on='common_index')

    # Eliminar las columnas innecesarias
    mto_df.drop(['SPEC_y', 'TYPE_CODE_y', 'FIRST_SIZE_y',
                'SECOND_SIZE_y', 'TAG_y'], axis=1, inplace=True)

    # Renombrando las columnas
    mto_df.rename(
        columns={'SPEC_x': 'SPEC', 'TYPE_CODE_x': 'TYPE_CODE', 'FIRST_SIZE_x': 'FIRST_SIZE', 'SECOND_SIZE_x': 'SECOND_SIZE', 'TAG_x': 'TAG'}, inplace=True)

    # Buscar pernos
    mto_df = define_bolts(mto_df, piping_class)

    return mto_df
