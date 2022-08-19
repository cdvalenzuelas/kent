import pandas as pd


from src.utils.replace_dot_by_comma import replace_dot_by_comma
from src.modules.compare_pid.valves_diferences.no_bom_valves import no_bom_valves
from src.modules.compare_pid.valves_diferences.no_pid_valves import no_pid_valves
from src.modules.compare_pid.valves_diferences.quantity_and_rating_diferences import quantity_and_rating_diferences


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

    # Traer únicamente las válvulas del P&ID
    pid_df = pid_df[pid_df['TAG'].notnull()]

    # Si el MTO no tiene válvulas, detener el análisis
    if mto_df.shape[0] == 0:
        # Si el P&ID tiene válvulas y el MTO no, entonces hay diferencias en las válvulas del proyecto
        if pid_df.shape[0] > 0:
            print(
                '❌ HAY DIFERENCIAS ENTRE LAS VÁLVULAS REPORTADAS POR EL B.O.M Y EL P&ID, EL MTO NO TIENE VÁLVULAS PERO EL P&ID SI LAS CONTEMPLA.\n')

        return

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

    # Eliminar el common_index
    merge_df.drop(['common_index'], inplace=True, axis=1)

    # De aquí en adelante se van a diferenciar tres grupos de válvulas

    # Válvulas que aparecen el el P&ID pero no en el BOM
    merge_df_group_1 = merge_df[(merge_df['LINE_NUM_x'].isnull())]

    if merge_df_group_1.shape[0] > 0:
        merge_df_group_1['common_index'] = merge_df_group_1[[
            'LINE_NUM_y', 'QTY_y', 'TYPE_CODE_y', 'FIRST_SIZE_NUMBER_y', 'RATING_y', 'SPEC_y']].apply(no_bom_valves, axis=1)

    # Válvulas que aparecen en el BOM pero no en el P&ID
    merge_df_group_2 = merge_df[(merge_df['LINE_NUM_y'].isnull())]

    if merge_df_group_2.shape[0] > 0:
        merge_df_group_2['common_index'] = merge_df_group_2[[
            'LINE_NUM_x', 'QTY_x', 'TYPE_CODE_x', 'FIRST_SIZE_NUMBER_x', 'RATING_x', 'SPEC_x']].apply(no_pid_valves, axis=1)

    # Válvulas que aparecen en los dos lados
    merge_df_group_3 = merge_df[(merge_df['LINE_NUM_y'].notnull()) & (
        merge_df['LINE_NUM_x'].notnull())]

    if merge_df_group_3.shape[0] > 0:
        merge_df_group_3['common_index'] = merge_df_group_3[[
            'LINE_NUM_x', 'TYPE_CODE_x', 'FIRST_SIZE_NUMBER_x', 'SPEC_x', 'QTY_x', 'QTY_y', 'RATING_x', 'RATING_y']].apply(quantity_and_rating_diferences, axis=1)

    # Concatenar todos los dtataframes
    merge_df = pd.concat(
        [merge_df_group_1, merge_df_group_2, merge_df_group_3], axis=0)

    # Ver cuantas válvulas tienen diferencias
    merge_df = merge_df[(merge_df['common_index'] == 'difference')]

    # Si no hay diferencias (según el paso anterior) en válvulas dejar de hacer el análisis
    if merge_df.shape[0] == 0:
        print(
            '✅ NO HAY DIFERENCIAS ENTRE LAS VÁLVULAS REPORTADAS POR EL B.O.M Y EL P&ID\n')
    # Si hay alguna diferencia generar un archivo temporal que de más luces
    else:
        print(
            '❌ HAY DIFERENCIAS ENTRE LAS VÁLVULAS REPORTADAS POR EL B.O.M Y EL P&ID\n')

    return
