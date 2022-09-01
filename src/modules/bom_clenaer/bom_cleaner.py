import pandas as pd

from src.modules.bom_clenaer.pipes_modifier import pipe_qty
from src.modules.bom_clenaer.nipples_modifier import nipple_second_size
from src.modules.diagnostic.diagnostic import diagnostic
from src.utils.replace_spaces_by_dash import replace_spaces_by_dash


# (VALEC17) Crea una columna comun entre el piping class y el bom
def concat_colums(row):
    return f'{row[0]} {row[1]} {row[2]} {row[3]} {row[4]}'


# (VALEC17) Define el tipo de unidades para cada tipo de elemento
def units(TYPE):
    if TYPE == 'PP':
        return 'm'
    else:
        return 'e.a'

# (VALEC17) Corregir el peso de las válvulas y dejar el que aparece en el bom


def valves_weight(row):
    weight_x, weight_y, type_element, qty = row

    if type_element == 'VL':
        return round(weight_x / qty, 2)
    else:
        return weight_y


# (VALEC17) Arreglar los nombres de de las líneas basdas en si son entrerradas y/o prefabricadas
def fix_line_num(line_num):
    line_num = line_num.replace('(U)', '').replace('(P)', '')

    return line_num


# (VALEC17) Dejar los pesos que vienen en el BOM
def bom_cleaner(bom, piping_class, piping_class_valves_weights):
    # (VALEC17) Llenar los pesos y longitudes vacías con 0
    bom['LENGTH'].fillna(0, inplace=True)
    bom['WEIGHT'].fillna(0, inplace=True)

    # (VALEC17) Llenar los N.A con guines
    bom.fillna('-', inplace=True)

    # (VALEC17) Se deja la longitud de los niples como segundo tamaño
    bom['RED_NOM'] = bom[['LENGTH', 'DB_CODE', 'RED_NOM']].apply(
        nipple_second_size, axis=1)

    # (VALEC17) Se deja la longitud de las tuberías como cantidad y se deja en el entero más cercano
    bom['QTY'] = bom[['LENGTH', 'DB_CODE', 'QTY']].apply(pipe_qty, axis=1)

    # (VALEC17) Se reemplazan los espacios por "guiones" en los tamaños combinados (ejemplo 1 1/2 se convierte en 1-1/2)
    bom['MAIN_NOM'] = bom['MAIN_NOM'].apply(replace_spaces_by_dash)
    bom['RED_NOM'] = bom['RED_NOM'].apply(replace_spaces_by_dash)

    # (VALEC17) Eliminar columnas innecesarias
    bom.drop(['MARK', 'THK_NOM', 'SIZE', 'DESCRIPTION'], axis=1, inplace=True)

    # (VALEC17) Se crean los índices del BOM y del piping class
    # (VALEC17) OJO AQUI SE DEBE PONER ES SHORT DESCRIPTIOOOOOOOOO!!!!!!!! CON ESO SE COMPRUEBAN ERRORES
    bom['common_index'] = bom[['SPEC_FILE', 'DB_CODE', 'MAIN_NOM',
                               'RED_NOM', 'TAG']].apply(concat_colums, axis=1)

    # (VALEC17) Se crean los índices del BOM y del piping class
    # (VALEC17) OJO AQUI SE DEBE PONER ES SHORT DESCRIPTIOOOOOOOOO!!!!!!!! CON ESO SE COMPRUEBAN ERRORES
    piping_class['common_index'] = piping_class[[
        'SPEC', 'TYPE_CODE', 'FIRST_SIZE', 'SECOND_SIZE', 'TAG']].apply(concat_colums, axis=1)

    # (VALEC17) Hacer un join entre el bom y el piping class para generar el mto
    mto_df = pd.merge(bom, piping_class, how='left', on='common_index')

    # (VALEC17) Corregir el peso de válvulas
    if not piping_class_valves_weights:
        mto_df['WEIGHT_y'] = mto_df[['WEIGHT_x', 'WEIGHT_y',
                                     'TYPE', 'QTY']].apply(valves_weight, axis=1)

    # (VALEC17) OJO EL DEFINE DIGANOSTIC DEBERÍA COJER UN ARCHIVO LIMPIO Y LLENARLO CON TODAD LAS FICIONES (BORRAR LOS ARCHIVOS DE INPUTS CADA VEZ QUE SE CORRA LA INFORMACIÓN)
    diagnostic(mto_df)

    # (VALEC17) Eliminando columnas innecesarias
    mto_df.drop(['WEIGHT_x', 'LENGTH', 'SHORT_DESC', 'SPEC_FILE', 'DB_CODE',
                'MAIN_NOM', 'RED_NOM', 'TAG_x', 'DESCRIPTION'], axis=1, inplace=True)

    # (VALEC17) Renombrando el SHORT_DESCRIPTION como DESCRIPTION
    mto_df.rename(
        columns={'SHORT_DESCRIPTION': 'DESCRIPTION', 'TAG_y': 'TAG', 'WEIGHT_y': 'WEIGHT'}, inplace=True)

    # (VALEC17) Creando la columna units
    mto_df['UNITS'] = mto_df['TYPE'].apply(units)

    # (VALEC17) Definir si el elemento está enterrado
    mto_df['UNDERGROUND'] = mto_df['LINE_NUM'].apply(
        lambda line_num: '(U)' in line_num)

    # (VALEC17) Definir si la línea es prefabricada
    mto_df['PRE_MANUFACTURING'] = mto_df['LINE_NUM'].apply(
        lambda line_num: '(P)' in line_num)

    # (VALEC17) Arreglar los nombres de línea
    mto_df['LINE_NUM'] = mto_df['LINE_NUM'].apply(fix_line_num)

    mto_df.fillna('-', inplace=True)

    return mto_df
