import pandas as pd

from src.modules.bom_clenaer.pipes_modifier import pipe_qty
from src.modules.bom_clenaer.nipples_modifier import nipple_second_size
from src.modules.diagnostic.diagnostic import diagnostic
from src.clients.cenit.piping_class.cenit_piping_class import cenit_piping_class
from src.utils.replace_spaces_by_dash import replace_spaces_by_dash


# Crea una columna comun entre el piping class y el bom
def concat_colums(row):
    return f'{row[0]} {row[1]} {row[2]} {row[3]} {row[4]}'


# Define el tipo de unidades para cada tipo de elemento
def units(TYPE):
    if TYPE == 'PP':
        return 'm'
    else:
        return 'e.a'

# Corregir el peso de las válvulas y dejar el que aparece en el bom


def valves_weight(row):
    weight_x, weight_y, type_element, qty = row

    if type_element == 'VL':
        return round(weight_x / qty, 2)
    else:
        return weight_y


# Dejar los pesos que vienen en el BOM
def bom_cleaner():
    # Leer el BOM
    bom = pd.read_csv('./inputs/bom.csv')

    # Llenar los N.A con guines
    bom.fillna('-', inplace=True)

    # Se deja la longitud de los niples como segundo tamaño
    bom['RED_NOM'] = bom[['LENGTH', 'DB_CODE', 'RED_NOM']].apply(
        nipple_second_size, axis=1)

    # Se deja la longitud de las tuberías como cantidad y se deja en el entero más cercano
    bom['QTY'] = bom[['LENGTH', 'DB_CODE', 'QTY']].apply(pipe_qty, axis=1)

    # Se reemplazan los espacios por "guiones" en los tamaños combinados (ejemplo 1 1/2 se convierte en 1-1/2)
    bom['MAIN_NOM'] = bom['MAIN_NOM'].apply(replace_spaces_by_dash)
    bom['RED_NOM'] = bom['RED_NOM'].apply(replace_spaces_by_dash)

    # Eliminar columnas innecesarias
    bom.drop(['MARK', 'THK_NOM', 'SIZE', 'DESCRIPTION'], axis=1, inplace=True)

    # Se crean los índices del BOM y del piping class
    # OJO AQUI SE DEBE PONER ES SHORT DESCRIPTIOOOOOOOOO!!!!!!!! CON ESO SE COMPRUEBAN ERRORES
    bom['common_index'] = bom[['SPEC_FILE', 'DB_CODE', 'MAIN_NOM',
                               'RED_NOM', 'TAG']].apply(concat_colums, axis=1)

    # Extraer el piping class
    piping_class = cenit_piping_class()

    # Se crean los índices del BOM y del piping class
    # OJO AQUI SE DEBE PONER ES SHORT DESCRIPTIOOOOOOOOO!!!!!!!! CON ESO SE COMPRUEBAN ERRORES
    piping_class['common_index'] = piping_class[[
        'SPEC', 'TYPE_CODE', 'FIRST_SIZE', 'SECOND_SIZE', 'TAG']].apply(concat_colums, axis=1)

    # Hacer un join entre el bom y el piping class para generar el mto
    mto_df = pd.merge(bom, piping_class, how='left', on='common_index')

    # Corregir el peso de válvulas
    # mto_df['WEIGHT_y'] = mto_df[['WEIGHT_x', 'WEIGHT_y',
    # 'TYPE', 'QTY']].apply(valves_weight, axis=1)

    # Por aqupí se hace la comparación OJOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    # OJO EL DEFINE DIGANOSTIC DEBERÍA COJER UN ARCHIVO LIMPIO Y LLENARLO CON TODAD LAS FICIONES (BORRAR LOS ARCHIVOS DE INPUTS CADA VEZ QUE SE CORRA LA INFORMACIÓN)
    diagnostic(mto_df)

    # Eliminando columnas innecesarias
    mto_df.drop(['WEIGHT_x', 'LENGTH', 'SHORT_DESC', 'SPEC_FILE', 'DB_CODE',
                'MAIN_NOM', 'RED_NOM', 'TAG_x', 'DESCRIPTION'], axis=1, inplace=True)

    # Renombrando el SHORT_DESCRIPTION como DESCRIPTION
    mto_df.rename(
        columns={'SHORT_DESCRIPTION': 'DESCRIPTION', 'TAG_y': 'TAG', 'WEIGHT_y': 'WEIGHT'}, inplace=True)

    # Creando la columna units
    mto_df['UNITS'] = mto_df['TYPE'].apply(units)

    mto_df.fillna('-', inplace=True)

    return mto_df