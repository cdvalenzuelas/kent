import pandas as pd
import os
import re


# se hace un diagnśtico de los campos
def mto_diagnostic(row):
    item, line_num, type_code, short_desc, short_description, weight_x, weight_y, length, bolt_length, qty, bolt_weight, first_size, bolt_diameter, second_size, rating = row

    # Cambiar las descripciones
    short_desc_2 = str.upper(str(short_desc))
    short_desc_2 = re.sub(' ', '', short_desc_2)
    short_desc_2 = re.sub('-', '', short_desc_2)

    short_description_2 = str.upper(str(short_description))
    short_description_2 = re.sub(' ', '', short_description_2)
    short_description_2 = re.sub('-', '', short_description_2)

    # Cambiar el second_size
    second_size = f'{int(bolt_length)}mm ({first_size}, #{rating})' if type_code == 'BOLT' else second_size
    second_size = '' if second_size == '-' else f'x{second_size}'

    # Cambiar el first_size
    first_size = bolt_diameter if type_code == 'BOLT' else first_size

    # Empezar a crear el diagnóstico
    mto_diagnostic = ''

    # DESCRIPTION Diagnostic
    if short_desc_2 != short_description_2:
        mto_diagnostic += f'* La DESCRIPTION no coincide, en el BOM es "{short_desc}" y en el piping_class es "{short_description}". Se deben revisar los isométricos\n'

    # PESOS UNITARIOS diqagnostic (Evidenciar una variación mayor al 5% del peso verdadero)
    if type_code in ['PE', 'BE', 'TE']:
        if 1000*weight_x/length >= 1.05*float(weight_y) or 1000*weight_x/length <= 0.95*float(weight_y):
            print(item)
            mto_diagnostic += f'* El WEIGHT_PER_UNIT no coincide, en el BOM es {1000*weight_x/length}kg ({weight_x}kg totales) y en el piping_class es {weight_y*length/1000}kg ({weight_y*qty}kg totales). Se deben revisar los isométricos \n'
    elif type_code == 'BOLT':
        if weight_x/qty >= 1.05*float(bolt_weight) or weight_x/qty <= 0.95*float(bolt_weight):
            if weight_y > 0:
                mto_diagnostic += f'* El WEIGHT_PER_UNIT no coincide, en el BOM es {weight_x/qty}kg ({weight_x}kg totales) y en el piping_class es {weight_y}kg ({weight_y*qty}kg totales). Se deben revisar los isométricos \n'
    else:
        if weight_x/qty >= 1.05*float(weight_y) or weight_x/qty <= 0.95*float(weight_y):
            if weight_y > 0:
                mto_diagnostic += f'* El WEIGHT_PER_UNIT no coincide, en el BOM es {weight_x}kg ({weight_x*qty}kg totales) y en el piping_class es {weight_y}kg ({weight_y*qty}kg totales). Se deben revisar los isométricos \n'

    # Ver diferencias en longitudes de pernos
    if type_code == 'BOLT' and length != bolt_length:
        mto_diagnostic += f'* La longitud de los pernos no coincide, en el BOM es de {length}mm y en el piping_class es de {bolt_length}mm. Se deben revisar los isométricos \n'

    # Ver si alguna tubería se puede sustituir con un niple
    if type_code in ['PE', 'BE', 'TE'] and length <= 200:
        mto_diagnostic += f'* La longitud de la tubería es muy corta ({length}mm), podría ser un niple. Revisar si se puede cambiar \n'

    # Verificar longitudes de pernos si existe un equipo tipo wafer
    if type_code in ['F8', 'BTY']:
        mto_diagnostic += f'* Este es un equipo tipo wafer vefificar pernos.\n'

    # Escribir en el archivo
    if mto_diagnostic != '':
        mto_diagnostic = f'ITEM {item}: {line_num} , {type_code}, {first_size}{second_size}\n---------------------------------------\n{mto_diagnostic}\n'

    if str(short_description) != 'nan':
        with open('./output/diagnostic.txt', mode='a') as f:
            f.write(mto_diagnostic)

    return item


# Crea una columna comun entre el mto y los bolt
def concat_bolt_index(row):
    first_size, rating, face = row

    rating = str(rating)

    rating = re.sub('[.]0', '', rating)

    return f'{first_size} {rating} {face}'


def define_diagnostic(mto_df):
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

    # Eliminar el archivo de diagnostic
    try:
        os.remove('./output/diagnostic.txt')
    except:
        print('EL ARCHIVO "diagnostic.txt" no existe en el proyecto')

    mto_df = mto_df[['INDEX', 'LINE_NUM', 'TYPE_CODE', 'SHORT_DESC', 'SHORT_DESCRIPTION', 'WEIGHT_x',
                    'WEIGHT_y', 'LENGTH', 'BOLT_LENGTH', 'QTY', 'BOLT_WEIGHT', 'FIRST_SIZE', 'BOLT_DIAMETER', 'SECOND_SIZE', 'RATING_x']]

    mto_df['INDEX'] = mto_df[['INDEX', 'LINE_NUM', 'TYPE_CODE', 'SHORT_DESC', 'SHORT_DESCRIPTION', 'WEIGHT_x',
                              'WEIGHT_y', 'LENGTH', 'BOLT_LENGTH', 'QTY', 'BOLT_WEIGHT', 'FIRST_SIZE', 'BOLT_DIAMETER', 'SECOND_SIZE', 'RATING_x']].apply(mto_diagnostic, axis=1)
