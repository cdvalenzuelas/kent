import pandas as pd
import os


# se hace un diagnśtico de los campos
def mto_diagnostic(row):
    item, line_num, spec, type_x, type_code, description_x, first_size, second_size, sch_x, face_x, rating_x, qty, units, weight_per_unit, total_weight, tag, common_index, type_y, order, description_y, short_description, first_size_number, second_size_number, sch_y, face_y, rating_y, weight, area = row

    mto_diagnostic = ''

    # TYPE diagnostoc
    if type_x != type_y:
        mto_diagnostic += f'* El TYPE no coincide, en el mto es "{type_x}" y en el piping_class es "{type_y}". \n'

    # DESCRIPTION Diagnostic
    if description_x != short_description:
        mto_diagnostic += f'* La DESCRIPTION no coincide, en el mto es "{description_x}" y en el piping_class es "{short_description}". \n'

    # SCH diqagnostic
    if sch_x != sch_y:
        mto_diagnostic += f'* El SCH no coincide, en el mto es "{sch_x}" y en el piping_class es "{sch_y}". \n'

    # FACE diqagnostic
    if face_x != face_y:
        mto_diagnostic += f'* El FACE no coincide, en el mto es "{face_x}" y en el piping_class es "{face_y}". \n'

    # RATING diqagnostic
    if rating_x != rating_y:
        mto_diagnostic += f'* El RATING no coincide, en el mto es "{rating_x}" y en el piping_class es "{rating_y}". \n'

    # PESOS UNITARIOS diqagnostic (Evidenciar una variación mayor al 5% del peso verdadero)
    if weight_per_unit >= 1.05*float(weight) or weight_per_unit <= 0.95*float(weight):
        if weight > 0:
            mto_diagnostic += f'* El WEIGHT_PER_UNIT no coincide, en el mto es "{weight_per_unit}" y en el piping_class es "{weight}". \n'

    # Escribir en el archivo
    if mto_diagnostic != '':
        mto_diagnostic = f'ITEM {item}\n---------------------------------------\n{mto_diagnostic}\n'

    if str(type_y) != 'nan':
        with open('./output/diagnostic.txt', mode='a') as f:
            f.write(mto_diagnostic)

    return line_num


def define_diganostic(mto_df):
    # Crear un índice artificial
    index = pd.DataFrame({'INDEX': list(range(1, mto_df.shape[0] + 1))})

    # Unir el indice y el mto en un dataframe
    mto_df = pd.concat([index, mto_df], axis=1)

    # Hacer un diganóstico de los items
    mto_df['LINE_NUM'] = mto_df[['INDEX', 'LINE_NUM', 'SPEC', 'TYPE_x', 'TYPE_CODE', 'DESCRIPTION_x',
                                 'FIRST_SIZE', 'SECOND_SIZE', 'SCH_x', 'FACE_x', 'RATING_x', 'QTY',
                                 'UNITS', 'WEIGHT_PER_UNIT', 'TOTAL_WEIGHT', 'TAG', 'common_index',
                                 'TYPE_y', 'ORDER', 'DESCRIPTION_y', 'SHORT_DESCRIPTION', 'FIRST_SIZE_NUMBER',
                                 'SECOND_SIZE_NUMBER', 'SCH_y', 'FACE_y', 'RATING_y',
                                 'WEIGHT', 'AREA']].apply(mto_diagnostic, axis=1)

    mto_df.drop(['INDEX'], axis=1, inplace=True)

    return mto_df
