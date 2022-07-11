import pandas as pd


from src.utils.replace_dot_by_comma import replace_dot_by_comma
from src.modules.compare_pid.valves_diferences.diacnostic import diacnostic


# Función para hacer un merge
def common_index(row):
    line, spec, type_code, size, rating, qty, tag = row
    return f'{line} {spec} {type_code} {size} {rating} {qty} {tag}'


# Función para hacer un merge
def common_index_2(row):
    line, spec, type_code, size, tag = row
    return f'{line} {spec} {type_code} {size} {tag}'


def valves_diferences(bom_lines_unique, pid_lines_unique, mto_df, pid_df):
    # Hacer una copia de los dataframes
    mto_df = mto_df.copy()
    pid_df = pid_df.copy()

    # Sacar únicamente las válvulas del MTO
    mto_df = mto_df[(mto_df['TYPE']) == 'VL']

    # Si existen válvulas, comparar válvulas
    if mto_df.shape[0] > 0:

        # Traer únicamente las válvulas del P&ID
        pid_df = pid_df[pid_df['SPEC'].notnull()]

        # Reemplazar los puntos por comas en el size del p&id
        pid_df['FIRST_SIZE_NUMBER'] = pid_df['FIRST_SIZE_NUMBER'].apply(
            replace_dot_by_comma)

        pid_df['RATING'] = pid_df['RATING'].apply(
            replace_dot_by_comma)

        pid_df['QTY'] = pid_df['QTY'].apply(
            replace_dot_by_comma)

        mto_df['FIRST_SIZE_NUMBER'] = mto_df['FIRST_SIZE_NUMBER'].apply(
            replace_dot_by_comma)

        mto_df['RATING'] = mto_df['RATING'].apply(
            replace_dot_by_comma)

        mto_df['QTY'] = mto_df['QTY'].apply(
            replace_dot_by_comma)

        # Crear un índice común entre el bom y el p&id
        mto_df['common_index'] = mto_df[['LINE_NUM', 'SPEC', 'TYPE_CODE',
                                        'FIRST_SIZE_NUMBER', 'RATING', 'QTY', 'TAG']].apply(common_index, axis=1)

        pid_df['common_index'] = pid_df[['LINE_NUM', 'SPEC', 'TYPE_CODE',
                                        'FIRST_SIZE_NUMBER', 'RATING', 'QTY', 'TAG']].apply(common_index, axis=1)

        # Hacer el Merge
        merge_df = pd.merge(mto_df, pid_df, how='outer', on='common_index')

        # Dejar únicamente las que no cinciden, es decir elminar las válvulas que coinciden en todo
        merge_df = merge_df[(merge_df['QTY_x'].isnull()) |
                            (merge_df['QTY_y'].isnull())]

        # Verifica si hay diferencias  XXXXXXXXX
        if merge_df.shape[0] > 0:

            # Eliminar el common_index
            merge_df.drop(['common_index'], inplace=True, axis=1)

            # Redefinir MTO
            mto_df = merge_df[merge_df['LINE_NUM_x'].notnull()]

            mto_df = mto_df[['LINE_NUM_x', 'SPEC_x', 'TYPE_CODE_x', 'FIRST_SIZE_NUMBER_x',
                            'RATING_x', 'QTY_x', 'TAG_x']]

            mto_df.rename(columns={'LINE_NUM_x': 'LINE_NUM', 'SPEC_x': 'SPEC', 'TYPE_CODE_x': 'TYPE_CODE', 'FIRST_SIZE_NUMBER_x': 'FIRST_SIZE_NUMBER',
                                   'RATING_x': 'RATING', 'QTY_x': 'QTY', 'TAG_x': 'TAG'}, inplace=True)

            # Redefinir P&ID
            pid_df = merge_df[merge_df['LINE_NUM_x'].isnull()]

            pid_df = pid_df[['LINE_NUM_y', 'SPEC_y', 'TYPE_CODE_y', 'FIRST_SIZE_NUMBER_y',
                            'RATING_y', 'QTY_y', 'TAG_y']]

            pid_df.rename(columns={'LINE_NUM_y': 'LINE_NUM', 'SPEC_y': 'SPEC', 'TYPE_CODE_y': 'TYPE_CODE', 'FIRST_SIZE_NUMBER_y': 'FIRST_SIZE_NUMBER',
                                   'RATING_y': 'RATING', 'QTY_y': 'QTY', 'TAG_y': 'TAG'}, inplace=True)

            # Crer un índice para comparar si hay hay diferencias en cantidades y ratings
            mto_df['common_index'] = mto_df[['LINE_NUM', 'SPEC', 'TYPE_CODE',
                                            'FIRST_SIZE_NUMBER', 'TAG']].apply(common_index_2, axis=1)

            pid_df['common_index'] = pid_df[['LINE_NUM', 'SPEC', 'TYPE_CODE',
                                            'FIRST_SIZE_NUMBER', 'TAG']].apply(common_index_2, axis=1)

            # Hacer el nuevo merge
            merge_df = pd.merge(mto_df, pid_df, how='outer', on='common_index')

            ''' # Extraer las válvulas que no se encontraron
            merge_df = merge_df[(merge_df['LINE_NUM_x'].isnull()) | (
                merge_df['LINE_NUM_y'].isnull())] '''

            # Saber si se imprime el archivo temporales o no
            if merge_df.shape[0] > 0:
                # Hacer un diagnóstico sobre cada una de las válvulas
                merge_df['common_index'] = merge_df[['LINE_NUM_x', 'SPEC_x', 'TYPE_CODE_x', 'FIRST_SIZE_NUMBER_x',
                                                    'RATING_x', 'QTY_x', 'LINE_NUM_y', 'SPEC_y',
                                                     'TYPE_CODE_y', 'FIRST_SIZE_NUMBER_y', 'RATING_y', 'QTY_y']].apply(diacnostic, axis=1, pid_lines_unique=pid_lines_unique, bom_lines_unique=bom_lines_unique)

                merge_df = merge_df[(merge_df['common_index'] == 'difference')]

                # Si hay diferencias en válvulas
                if merge_df.shape[0] > 0:

                    print(
                        '❌  HAY DIFERENCIAS ENTRE LAS VÁLVULAS REPORTADAS POR EL B.O.M Y EL P&ID\n')

                    merge_df.to_csv('./output/p&id_temp.csv')
                else:
                    print(
                        '✅  NO HAY DIFERENCIAS ENTRE LAS VÁLVULAS REPORTADAS POR EL B.O.M Y EL P&ID\n')
            else:
                print(
                    '✅  NO HAY DIFERENCIAS ENTRE LAS VÁLVULAS REPORTADAS POR EL B.O.M Y EL P&ID\n')
