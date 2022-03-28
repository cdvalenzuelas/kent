import pandas as pd
import os


# se hace un diagnśtico de los campos
def mto_diagnostic(row):
    item, short_desc, short_description, weight_x, weight_y, length, second_size, second_size_number = row

    mto_diagnostic = ''

    # DESCRIPTION Diagnostic
    if short_desc != short_description:
        mto_diagnostic += f'* La DESCRIPTION no coincide, en el BOM es "{short_desc}" y en el piping_class es "{short_description}". \n'

    # PESOS UNITARIOS diqagnostic (Evidenciar una variación mayor al 5% del peso verdadero)
    if weight_x >= 1.05*float(weight_y) or weight_x <= 0.95*float(weight_y):
        if weight_y > 0:
            mto_diagnostic += f'* El WEIGHT_PER_UNIT no coincide, en el BOM es "{weight_x}" y en el piping_class es "{weight_y}". \n'

    # Escribir en el archivo
    if mto_diagnostic != '':
        mto_diagnostic = f'ITEM {item}\n---------------------------------------\n{mto_diagnostic}\n'

    if str(short_description) != 'nan':
        with open('./output/diagnostic.txt', mode='a') as f:
            f.write(mto_diagnostic)

    return item


def define_diagnostic(mto_df):
    # Crear un índice artificial
    index = pd.DataFrame({'INDEX': list(range(1, mto_df.shape[0] + 1))})

    # Unir el indice y el mto en un dataframe
    mto_df = pd.concat([index, mto_df], axis=1)

    # Eliminar el archivo de diagnostic
    try:
        os.remove('./output/diagnostic.txt')
    except:
        print('EL ARCHIVO "diagnostic.txt" no existe en el proyecto')

    mto_df = mto_df[['INDEX', 'SHORT_DESC', 'SHORT_DESCRIPTION', 'WEIGHT_x',
                    'WEIGHT_y', 'LENGTH', 'SECOND_SIZE', 'SECOND_SIZE_NUMBER']]

    mto_df['INDEX'] = mto_df[['INDEX', 'SHORT_DESC', 'SHORT_DESCRIPTION', 'WEIGHT_x',
                              'WEIGHT_y', 'LENGTH', 'SECOND_SIZE', 'SECOND_SIZE_NUMBER']].apply(mto_diagnostic, axis=1)
