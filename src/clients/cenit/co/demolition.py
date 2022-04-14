import pandas as pd
import re


from src.clients.cenit.piping_class.cenit_piping_class import cenit_piping_class
from src.modules.mto_does_not_exist.pipes_modifier import pipe_qty
from src.modules.mto_does_not_exist.nipples_modifier import nipple_second_size
from src.clients.cenit.piping_class.cenit_piping_class import cenit_piping_class
from src.clients.cenit.co.utils import common_index, def_note
from src.utils.replace_spaces_by_dash import replace_spaces_by_dash


# Crea una columna comun entre el piping class y el bom
def concat_colums(row):
    spec, type_code, first_size, second_size, tag = row
    return f'{spec} {type_code} {first_size} {second_size} {tag}'


def demolition_cleaner(demolition_df):
    # Llenar los N.A con guines
    demolition_df.fillna('-', inplace=True)

    # Se deja la longitud de los niples como segundo tamaño
    demolition_df['RED_NOM'] = demolition_df[['LENGTH', 'DB_CODE', 'RED_NOM']].apply(
        nipple_second_size, axis=1)

    # Se deja la longitud de las tuberías como cantidad y se deja en el entero más cercano
    demolition_df['QTY'] = demolition_df[['LENGTH', 'DB_CODE', 'QTY']].apply(
        pipe_qty, axis=1)

    # Se reemplazan los espacios por "guiones" en los tamaños combinados (ejemplo 1 1/2 se convierte en 1-1/2)
    demolition_df['MAIN_NOM'] = demolition_df['MAIN_NOM'].apply(
        replace_spaces_by_dash)
    demolition_df['RED_NOM'] = demolition_df['RED_NOM'].apply(
        replace_spaces_by_dash)

    # Eliminar columnas innecesarias
    demolition_df.drop(
        ['MARK', 'THK_NOM', 'SIZE', 'DESCRIPTION'], axis=1, inplace=True)

    # Se crean los índices del BOM y del piping class
    # OJO AQUI SE DEBE PONER ES SHORT DESCRIPTIOOOOOOOOO!!!!!!!! CON ESO SE COMPRUEBAN ERRORES
    demolition_df['common_index'] = demolition_df[['SPEC_FILE', 'DB_CODE', 'MAIN_NOM',
                                                   'RED_NOM', 'TAG']].apply(concat_colums, axis=1)

    # Extraer el piping class
    piping_class = cenit_piping_class()

    # Se crean los índices del BOM y del piping class
    # OJO AQUI SE DEBE PONER ES SHORT DESCRIPTIOOOOOOOOO!!!!!!!! CON ESO SE COMPRUEBAN ERRORES
    piping_class['common_index'] = piping_class[[
        'SPEC', 'TYPE_CODE', 'FIRST_SIZE', 'SECOND_SIZE', 'TAG']].apply(concat_colums, axis=1)

    # Hacer un join entre el bom y el piping class para generar el mto
    demolition_df = pd.merge(demolition_df, piping_class,
                             how='left', on='common_index')

    # Crear registro de items sin identificar
    demolition_df_na = demolition_df[(demolition_df['DESCRIPTION'].isnull()) | (
        demolition_df['DESCRIPTION'] == '-')]

    if demolition_df_na.shape[0] > 0:
        demolition_df_na = demolition_df_na[[
            'LINE_NUM', 'QTY', 'common_index']]

        demolition_df_na.to_csv('./output/demolition_temp.csv', index=True)

        print('❌ HAY ELEMENTOS DEL ARCHIVO demolition.csv NO TIENEN PROPIEDADES DE DEMOLICIÓN O NO ESTÁN EN EL PIPING CLASS\n')
    else:
        print('✅ TODOS LOS ELEMENTOS DEL ARCHIVO demolition.csv TIENEN PROPIEDADES DE DEMOLICIÓN Y ESTÁN EN EL PIPING CLASS\n')

        # Eliminando columnas innecesarias
    demolition_df.drop(['WEIGHT_x', 'LENGTH', 'SHORT_DESC', 'SPEC_FILE', 'DB_CODE',
                        'MAIN_NOM', 'RED_NOM', 'TAG_x', 'DESCRIPTION'], axis=1, inplace=True)

    # Renombrando el SHORT_DESCRIPTION como DESCRIPTION
    demolition_df.rename(
        columns={'SHORT_DESCRIPTION': 'DESCRIPTION', 'TAG_y': 'TAG', 'WEIGHT_y': 'WEIGHT'}, inplace=True)

    demolition_df.fillna('-', inplace=True)

    # Dejar únicamente las columnas necesarias
    demolition_df = demolition_df[['TYPE', 'WEIGHT', 'DEMOLITION_DESCRIPTION']]

    return demolition_df


# Definir la descripción de la demolición en función del tipo de elemento
def def_demolition_description(row, method):
    type_element, demolition_description, weight = row

    if type_element == 'VL':
        if weight <= 200:
            return 'DESMANTELAMIENTO DE VÁLVULAS CUYO PESO SEA ≤ 200 KG(INCLUYE TRANSPORTE Y DISPOSICIÓN FINAL)'
        elif weight > 200 and weight <= 500:
            return 'DESMANTELAMIENTO DE VÁLVULA CUYO PESO SEA > 200 KG HASTA 500 KG (INCLUYE TRANSPORTE Y DISPOSICIÓN FINAL)'
        elif weight > 500 and weight <= 1000:
            return 'DESMANTELAMIENTO DE VÁLVULA CUYO PESO SEA > 500 KG HASTA 1.000 KG (INCLUYE TRANSPORTE Y DISPOSICIÓN FINAL)'
        elif weight > 1000 and weight <= 3000:
            return 'DESMANTELAMIENTO DE VÁLVULA CUYO PESO SEA ENTRE 1.001 KG HASTA 3.000 KG (INCLUYE TRANSPORTE Y DISPOSICIÓN FINAL)'
        elif weight > 3000 and weight <= 6000:
            return 'DESMANTELAMIENTO DE VÁLVULA CUYO PESO SEA ENTRE 3.001 KG HASTA 6.000 KG (INCLUYE TRANSPORTE Y DISPOSICIÓN FINAL)'
        else:
            return 'DESMANTELAMIENTO DE VÁLVULA CUYO PESO SEA > 6.000 KG (INCLUYE TRANSPORTE Y DISPOSICIÓN FINAL)'
    else:
        if method == 'hot':
            return re.sub('CORTE EN FRÍO', 'OXICORTE', demolition_description)
        else:
            return demolition_description


# Define la cantidad de los elementos nuevos
def def_qty(row):
    qty_x, qty_y = row

    if qty_y == '-':
        return qty_x
    else:
        return qty_y

# OJO EL DEMOLITION TAMBIÉN PUEDE VENIR EN FORMA DE MTO


def demolition(method):
    try:
        # Leer el archivo de demolición
        demolition_df = pd.read_csv('./inputs/demolition.csv')

        print('💡 VERIFICAR QUE EL ARCHIVO demolition.csv SEA EL CORRECTO\n')

        # Limpiar el demolition.csv
        demolition_df = demolition_cleaner(demolition_df)

        # Definir el demolition descrption según el type
        demolition_df['DEMOLITION_DESCRIPTION'] = demolition_df[[
            'TYPE', 'DEMOLITION_DESCRIPTION', 'WEIGHT']].apply(def_demolition_description, axis=1, method=method)

        # Se suman las cantidades
        demolition_df = demolition_df.groupby(['DEMOLITION_DESCRIPTION'], as_index=False)[
            ['WEIGHT']].agg(WEIGHT=('WEIGHT', sum))

        # Leer el archivo de cantidades de obra creadas
        co_template = pd.read_csv('./output/co.csv')

        # Crear índices comunes para hacer un merge
        demolition_df['common_index'] = demolition_df['DEMOLITION_DESCRIPTION'].apply(
            common_index)

        co_template['common_index'] = co_template['DESCRIPTION'].apply(
            common_index)

        # Hacer un merge full
        demolition_df = pd.merge(
            co_template, demolition_df, on='common_index', how='outer')

        # Llenar espacios vacío
        demolition_df.fillna('-', inplace=True)

        # Definir las cantidades
        demolition_df['QTY'] = demolition_df[[
            'QTY', 'WEIGHT']].apply(def_qty, axis=1)

        # Deninir si un elemento es nuevo o no
        demolition_df['NOTE'] = demolition_df[[
            'AREA', 'NOTE']].apply(def_note, axis=1)

        # Eliminando columnas inncesarias
        demolition_df.drop(['common_index', 'DEMOLITION_DESCRIPTION',
                            'WEIGHT'], inplace=True, axis=1)

        # Guardar el archivo creado
        demolition_df.to_csv('./output/co.csv', index=False)

    except:
        print('❌ NO EXISTE EL ARCHIVO "demolition.csv", NO SE PUEDEN CALCULAR LAS CANTIDADES DE OBRA DE DESMANTELAMIENTO\n')
