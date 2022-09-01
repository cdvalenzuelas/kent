import pandas as pd


from src.utils.replace_dot_by_comma import replace_dot_by_comma
from src.modules.compare_pid.valves_diferences.diacnostic import diacnostic


# (VALEC17) Función para hacer un merge
def common_index(row):
    line, spec, type_code, size, rating, qty, tag = row
    return f'{line} {spec} {type_code} {size} {rating} {qty} {tag}'


# (VALEC17) Función para hacer un merge
def common_index_2(row):
    line, spec, type_code, size, tag = row
    return f'{line} {spec} {type_code} {size} {tag}'


def valves_diferences(bom_lines_unique, pid_lines_unique, mto_df, pid_df):
    # (VALEC17) Hacer una copia de los dataframes
    mto_df = mto_df.copy()
    pid_df = pid_df.copy()

    # (VALEC17) Sacar únicamente las válvulas del MTO
    mto_df = mto_df[(mto_df['TYPE']) == 'VL']

    # (VALEC17) Traer únicamente las válvulas del P&ID
    pid_df = pid_df[pid_df['TAG'].notnull()]

    # (VALEC17) Si el MTO no tiene válvulas, detener el análisis
    if mto_df.shape[0] == 0:
        # (VALEC17) Si el P&ID tiene válvulas y el MTO no, entonces hay diferencias en las válvulas del proyecto
        if pid_df.shape[0] > 0:
            print(
                '❌ HAY DIFERENCIAS ENTRE LAS VÁLVULAS REPORTADAS POR EL B.O.M Y EL P&ID, EL MTO NO TIENE VÁLVULAS PERO EL P&ID SI LAS CONTEMPLA.\n')

        return

    # (VALEC17) Reemplazar los puntos por comas en el size del p&id
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

    # (VALEC17) Crear un índice común entre el bom y el p&id
    mto_df['common_index'] = mto_df[['LINE_NUM', 'SPEC', 'TYPE_CODE',
                                    'FIRST_SIZE_NUMBER', 'RATING', 'QTY', 'TAG']].apply(common_index, axis=1)

    pid_df['common_index'] = pid_df[['LINE_NUM', 'SPEC', 'TYPE_CODE',
                                    'FIRST_SIZE_NUMBER', 'RATING', 'QTY', 'TAG']].apply(common_index, axis=1)

    # (VALEC17) Hacer el Merge
    merge_df = pd.merge(mto_df, pid_df, how='outer', on='common_index')

    # (VALEC17) Dejar únicamente las que no cinciden, es decir elminar las válvulas que coinciden en todo
    merge_df = merge_df[(merge_df['QTY_x'].isnull()) |
                        (merge_df['QTY_y'].isnull())]

    # (VALEC17) Si no hay diferencias (según el paso anterior) en válvulas dejar de hacer el análisis
    if merge_df.shape[0] == 0:
        print(
            '✅ NO HAY DIFERENCIAS ENTRE LAS VÁLVULAS REPORTADAS POR EL B.O.M Y EL P&ID\n')
        return

    # (VALEC17) Eliminar el common_index
    merge_df.drop(['common_index'], inplace=True, axis=1)

    # (VALEC17) Redefinir MTO
    mto_df = merge_df[merge_df['LINE_NUM_x'].notnull()]

    mto_df = mto_df[['LINE_NUM_x', 'SPEC_x', 'TYPE_CODE_x', 'FIRST_SIZE_NUMBER_x',
                    'RATING_x', 'QTY_x', 'TAG_x']]

    mto_df.rename(columns={'LINE_NUM_x': 'LINE_NUM', 'SPEC_x': 'SPEC', 'TYPE_CODE_x': 'TYPE_CODE', 'FIRST_SIZE_NUMBER_x': 'FIRST_SIZE_NUMBER',
                           'RATING_x': 'RATING', 'QTY_x': 'QTY', 'TAG_x': 'TAG'}, inplace=True)

    # (VALEC17) Redefinir P&ID
    pid_df = merge_df[merge_df['LINE_NUM_x'].isnull()]

    pid_df = pid_df[['LINE_NUM_y', 'SPEC_y', 'TYPE_CODE_y', 'FIRST_SIZE_NUMBER_y',
                    'RATING_y', 'QTY_y', 'TAG_y']]

    pid_df.rename(columns={'LINE_NUM_y': 'LINE_NUM', 'SPEC_y': 'SPEC', 'TYPE_CODE_y': 'TYPE_CODE', 'FIRST_SIZE_NUMBER_y': 'FIRST_SIZE_NUMBER',
                           'RATING_y': 'RATING', 'QTY_y': 'QTY', 'TAG_y': 'TAG'}, inplace=True)

    # (VALEC17) Crer un índice para comparar si hay hay diferencias en cantidades y ratings
    mto_df['common_index'] = mto_df[['LINE_NUM', 'SPEC', 'TYPE_CODE',
                                    'FIRST_SIZE_NUMBER', 'TAG']].apply(common_index_2, axis=1)

    pid_df['common_index'] = pid_df[['LINE_NUM', 'SPEC', 'TYPE_CODE',
                                    'FIRST_SIZE_NUMBER', 'TAG']].apply(common_index_2, axis=1)

    # (VALEC17) Hacer el nuevo merge
    merge_df = pd.merge(mto_df, pid_df, how='outer', on='common_index')

    # (VALEC17) Si la diferencia radica en cantidades y ratings, aún así hay diferencias
    if merge_df.shape[0] == 0:
        print(
            '✅ NO HAY DIFERENCIAS ENTRE LAS VÁLVULAS REPORTADAS POR EL B.O.M Y EL P&ID\n')
        return

    # (VALEC17) Si hay diferencias entre ratings y cantidades seguir el análisis

    # (VALEC17) Hacer un diagnóstico sobre cada una de las válvulas
    merge_df['common_index'] = merge_df[['LINE_NUM_x', 'SPEC_x', 'TYPE_CODE_x', 'FIRST_SIZE_NUMBER_x',
                                        'RATING_x', 'QTY_x', 'LINE_NUM_y', 'SPEC_y',
                                         'TYPE_CODE_y', 'FIRST_SIZE_NUMBER_y', 'RATING_y', 'QTY_y']].apply(diacnostic, axis=1, pid_lines_unique=pid_lines_unique, bom_lines_unique=bom_lines_unique)

    # (VALEC17) Dejar únicamente las válvulas que tuvieron diferencias
    merge_df = merge_df[(merge_df['common_index'] == 'difference')]

    # (VALEC17) Si no hay diferencias de ningún tipo, parar el análisis
    if merge_df.shape[0] == 0:
        print(
            '✅ NO HAY DIFERENCIAS ENTRE LAS VÁLVULAS REPORTADAS POR EL B.O.M Y EL P&ID\n')
    # (VALEC17) Si hay alguna diferencia generar un archivo temporal que de más luces
    else:
        print(
            '❌ HAY DIFERENCIAS ENTRE LAS VÁLVULAS REPORTADAS POR EL B.O.M Y EL P&ID\n')
