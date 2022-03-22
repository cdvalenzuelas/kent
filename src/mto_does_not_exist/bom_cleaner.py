import pandas as pd
import re

from src.mto_does_not_exist.pipes_modifier import pipe_qty
from src.mto_does_not_exist.nipples_modifier import nipple_second_size, nipple_second_size_number


# Reemplaza los espacios por guines en los tamalños en pulgadas
def replace_spaces(size):
    return re.sub('[\s]', '-', str(size))


# Crea una columna comun entre el piping class y el bom
def concat_colums(row):
    return f'{row[0]} {row[1]} {row[2]} {row[3]} {row[4]}'


# Define el tipo de unidades para cada tipo de elemento
def units(TYPE):
    if TYPE == 'PP':
        return 'm'
    else:
        return 'e.a'


def bom_cleaner():
    # Leer el BOM
    bom = pd.read_csv('bom.csv')

    # Llenar los N.A con guines
    bom.fillna('-', inplace=True)

    # Se deja la longitud de los niples como segundo tamaño
    bom['RED_NOM'] = bom[['LENGTH', 'DB_CODE', 'RED_NOM']].apply(
        nipple_second_size, axis=1)

    # Se deja la longitud de las tuberías como cantidad y se deja en el entero más cercano
    bom['QTY'] = bom[['LENGTH', 'DB_CODE', 'QTY']].apply(pipe_qty, axis=1)

    # Se reemplazan los espacios por "guiones" en los tamaños combinados (ejemplo 1 1/2 se convierte en 1-1/2)
    bom['MAIN_NOM'] = bom['MAIN_NOM'].apply(replace_spaces)
    bom['RED_NOM'] = bom['RED_NOM'].apply(replace_spaces)

    # Eliminar columnas innecesarias
    bom.drop(['MARK', 'THK_NOM', 'SIZE', 'WEIGHT', 'LENGTH',
             'SHORT_DESC', 'DESCRIPTION'], axis=1, inplace=True)

    # Se crean los índices del BOM y del piping class
    # OJO AQUI SE DEBE PONER ES SHORT DESCRIPTIOOOOOOOOO!!!!!!!! CON ESO SE COMPRUEBAN ERRORES
    bom['common_index'] = bom[['SPEC_FILE', 'DB_CODE', 'MAIN_NOM',
                               'RED_NOM', 'TAG']].apply(concat_colums, axis=1)

    # Extraer el piping class
    CS2SA1 = pd.read_csv('./CENIT/PIPING_CLASS/CS2SA1.csv')
    CS3SA1 = pd.read_csv('./CENIT/PIPING_CLASS/CS3SA1.csv')
    CS5SA1 = pd.read_csv('./CENIT/PIPING_CLASS/CS5SA1.csv')
    CS6SA1 = pd.read_csv('./CENIT/PIPING_CLASS/CS6SA1.csv')
    CS1SC2 = pd.read_csv('./CENIT/PIPING_CLASS/CS1SC2.csv')

    piping_class = pd.concat([CS2SA1, CS3SA1, CS5SA1, CS6SA1, CS1SC2])

    # Se crean los índices del BOM y del piping class
    # OJO AQUI SE DEBE PONER ES SHORT DESCRIPTIOOOOOOOOO!!!!!!!! CON ESO SE COMPRUEBAN ERRORES
    piping_class['common_index'] = piping_class[[
        'SPEC', 'TYPE_CODE', 'FIRST_SIZE', 'SECOND_SIZE', 'TAG']].apply(concat_colums, axis=1)

    # Hacer un join entre el bom y el piping class para generar el mto
    mto_df = pd.merge(bom, piping_class, how='left', on='common_index')

    # Eliminando columnas innecesarias
    mto_df.drop(['SPEC_FILE', 'DB_CODE', 'MAIN_NOM',
                'RED_NOM', 'TAG_x', 'DESCRIPTION'], axis=1, inplace=True)

    # Renombrando el SHORT_DESCRIPTION como DESCRIPTION
    mto_df.rename(
        columns={'SHORT_DESCRIPTION': 'DESCRIPTION', 'TAG_y': 'TAG'}, inplace=True)

    # Creando la columna units
    mto_df['UNITS'] = mto_df['TYPE'].apply(units)

    return mto_df
