from cmath import pi
import pandas as pd

from src.modules.bom_clenaer.pipes_modifier import pipe_qty
from src.modules.bom_clenaer.nipples_modifier import nipple_second_size
from src.utils.replace_spaces_by_dash import replace_spaces_by_dash
from src.modules.bolts_modifier.bolts_modifier import bolts_modifier


# (VALEC17) Crea una columna comun entre el piping class y el bom
def concat_colums(row):
    spec, type_code, first_size, second_size, tag = row
    return f'{spec} {type_code} {first_size} {second_size} {tag}'


# (VALEC17) Arreglar los nombres de de las líneas basdas en si son entrerradas y/o prefabricadas
def fix_line_num(line_num):
    line_num = line_num.replace('(U)', '').replace('(F)', '')

    return line_num


# (VALEC17) Definir el peso o el volumen de la tubería a desmantelas o a abandonar
def def_weight(row):
    element_type, weight, qty, underground, forgiven, area = row

    if not forgiven:
        # (VALEC17) Si no es tubería olvidada que se cambie su peso
        return weight * qty
    else:

        if element_type == 'PP':
            # (VALEC17) Un dies porciento más que el volumen de la tubería
            return 1.1 * 0.25 * pi * qty * ((area * 0.001) ** 2)
        else:
            return 0


def demolition_cleaner(demolition_df, piping_class):
    # (VALEC17) Llenar los N.A con guines
    demolition_df.fillna('-', inplace=True)

    # (VALEC17) Se deja la longitud de los niples como segundo tamaño
    demolition_df['RED_NOM'] = demolition_df[['LENGTH', 'DB_CODE', 'RED_NOM']].apply(
        nipple_second_size, axis=1)

    # (VALEC17) Se deja la longitud de las tuberías como cantidad y se deja en el entero más cercano
    demolition_df['QTY'] = demolition_df[['LENGTH', 'DB_CODE', 'QTY']].apply(
        pipe_qty, axis=1)

    # (VALEC17) Se reemplazan los espacios por "guiones" en los tamaños combinados (ejemplo 1 1/2 se convierte en 1-1/2)
    demolition_df['MAIN_NOM'] = demolition_df['MAIN_NOM'].apply(
        replace_spaces_by_dash)
    demolition_df['RED_NOM'] = demolition_df['RED_NOM'].apply(
        replace_spaces_by_dash)

    # (VALEC17) Eliminar columnas innecesarias
    demolition_df.drop(
        ['MARK', 'THK_NOM', 'SIZE', 'DESCRIPTION'], axis=1, inplace=True)

    # (VALEC17) Se crean los índices del BOM y del piping class
    demolition_df['common_index'] = demolition_df[['SPEC_FILE', 'DB_CODE', 'MAIN_NOM',
                                                   'RED_NOM', 'TAG']].apply(concat_colums, axis=1)

    # (VALEC17) Se crean los índices del BOM y del piping class
    # (VALEC17) OJO AQUI SE DEBE PONER ES SHORT DESCRIPTIOOOOOOOOO!!!!!!!! CON ESO SE COMPRUEBAN ERRORES
    piping_class['common_index'] = piping_class[[
        'SPEC', 'TYPE_CODE', 'FIRST_SIZE', 'SECOND_SIZE', 'TAG']].apply(concat_colums, axis=1)

    # (VALEC17) Hacer un join entre el bom y el piping class para generar el mto
    demolition_df = pd.merge(demolition_df, piping_class,
                             how='left', on='common_index')

    # (VALEC17) Definir si el elemento está enterrado
    demolition_df['UNDERGROUND'] = demolition_df['LINE_NUM'].apply(
        lambda line_num: '(U)' in line_num)

    # (VALEC17) Definir si la línea es prefabricada
    demolition_df['FORGIVEN'] = demolition_df['LINE_NUM'].apply(
        lambda line_num: '(F)' in line_num)

    # (VALEC17) Arreglar los nombres de línea
    demolition_df['LINE_NUM'] = demolition_df['LINE_NUM'].apply(fix_line_num)

    # (VALEC17) A las válvulas se les asigna otro item de demolición
    demolition_df['DEMOLITION_DESCRIPTION'] = demolition_df.apply(
        lambda x: 'VL' if x['TYPE'] == 'VL' else x['DEMOLITION_DESCRIPTION'], axis=1)

    # (VALEC17) Crear registro de items sin identificar
    demolition_df_na = demolition_df[(demolition_df['DESCRIPTION'].isnull()) | (
        demolition_df['DESCRIPTION'] == '-') | (demolition_df['DEMOLITION_DESCRIPTION'] == '-')]

    if demolition_df_na.shape[0] > 0:
        demolition_df_na = demolition_df_na[[
            'LINE_NUM', 'QTY', 'common_index']]

        demolition_df_na.to_csv('./output/demolition_temp.csv', index=True)

        print('❌ HAY ELEMENTOS DEL ARCHIVO demolition.csv NO TIENEN PROPIEDADES DE DEMOLICIÓN O NO ESTÁN EN EL PIPING CLASS\n')
    else:
        print('✅ TODOS LOS ELEMENTOS DEL ARCHIVO demolition.csv TIENEN PROPIEDADES DE DEMOLICIÓN Y ESTÁN EN EL PIPING CLASS\n')

    # (VALEC17) Eliminando columnas innecesarias
    demolition_df.drop(['WEIGHT_x', 'LENGTH', 'SHORT_DESC', 'SPEC_FILE', 'DB_CODE',
                        'MAIN_NOM', 'RED_NOM', 'TAG_x', 'DESCRIPTION'], axis=1, inplace=True)

    # (VALEC17) Renombrando el SHORT_DESCRIPTION como DESCRIPTION
    demolition_df.rename(
        columns={'SHORT_DESCRIPTION': 'DESCRIPTION', 'TAG_y': 'TAG', 'WEIGHT_y': 'WEIGHT'}, inplace=True)

    demolition_df.fillna('-', inplace=True)

    # (VALEC17) Modificación por pernos
    demolition_df = bolts_modifier(mto_df=demolition_df)

    # (VALEC17) Ver si algunos elementos de la demolición tienen peso cero
    demolition_df_zero_weight = demolition_df[demolition_df['WEIGHT'] == 0]

    if demolition_df_zero_weight.shape[0] > 0:
        demolition_df_zero_weight.to_csv(
            './output/demolition_df_zero_weight.csv', index=True)

        print('❌ HAY ELEMENTOS DE DEMOLICIÓN QUE NO TIENEN PESO ASIGNADO.\n')
    else:
        print('✅ TODOS LOS ELEMENTOS DE DEMOLICIÓN TIENEN UN PESO ASIGNADO.\n')

    # (VALEC17) Dejar únicamente las columnas necesarias
    demolition_df = demolition_df[[
        'LINE_NUM', 'TYPE', 'WEIGHT', 'DEMOLITION_DESCRIPTION', 'QTY', 'UNDERGROUND', 'FORGIVEN', 'AREA']]

    demolition_df['WEIGHT'] = demolition_df[['TYPE', 'WEIGHT', 'QTY',
                                             'UNDERGROUND', 'FORGIVEN', 'AREA']].apply(def_weight, axis=1)

    return demolition_df
