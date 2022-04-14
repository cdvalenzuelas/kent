import pandas as pd


from src.utils.replace_dot_by_comma import replace_dot_by_comma


# Función para hacer un merge
def common_index(row):
    line, spec, type_code, size, rating, qty = row
    return f'{line} {spec} {type_code} {size} {rating} {qty}'


# Función para hacer un merge
def common_index_2(row):
    line, spec, type_code, size = row
    return f'{line} {spec} {type_code} {size}'


# Hacer un diagnótico sobre cada válvula
def diacnostic(row, pid_lines_unique, bom_lines_unique):
    line_x, spec_x, type_x, size_x, rating_x, qty_x, line_y, spec_y, type_y, size_y, rating_y, qty_y = row

    diacnostic_str = ''

    if str(line_x) != 'nan' and line_x not in bom_lines_unique:
        diacnostic_str = f"""
La línea {line_x} contiene {qty_x} válvulas de typo {type_x}, diámetro {size_x}", rating {rating_x}, y spec {spec_x}.
Éstas válvulas existen en el B.O.M pero no en el P&ID. Contrastar la maqueta con el P&ID. Es posible que la línea esté
mal nombrada en la maqueta, esté mal seleccionado el tipo de válvula, el diámetro, el rating o el spec con respecto al P&ID. 
        """

    if str(line_y) != 'nan' and line_y not in pid_lines_unique:
        diacnostic_str = f"""
La línea {line_y} contiene {qty_y} válvulas de tipo {type_y}, diámetro {size_y}", rating {rating_y} y spec {spec_y}.
Éstas válvulas existen en el P&ID pero no en el B.O.M. Es posible que éstas válvulas no se encuentren ruteadas o que
las líneas estén mal nombradas en la maqueta.
        """

    if str(line_x) != 'nan' and str(line_y) != 'nan':
        diacnostic_str = f"""
La línea {line_x} contiene válvulas de tipo {type_x}, diámetro {size_x}" y spec {spec_x}.
Las válvulas mensionadas anteriormente tienen diferencias en rating o cantidades."""

        rating_diff = ''
        qty_diff = ''

        # Ver diferencias en ratings
        if rating_x != rating_y:
            rating_diff = f"""
El rating no correspone, en el P&ID es {rating_y} pero por piping_class debería ser {rating_x}, se debe evaluar el P&ID (hablar con procesos)."""

        # Ver diferencias en cantidades
        if qty_x != qty_y:
            compare = 'más' if qty_x > qty_y else 'menos'
            qty_diff = f"""
Las cantidades no coinciden, en el B.O.M es {qty_x} y en P&ID es {qty_y}. Existen {compare} válvulas en la maqueta que en el P&ID."""

        if rating_diff and qty_diff:
            diacnostic_str = diacnostic_str + rating_diff + '\n' + qty_diff + '\n'
        elif rating_diff:
            diacnostic_str = diacnostic_str + rating_diff + '\n'
        elif qty_diff:
            diacnostic_str = diacnostic_str + qty_diff + '\n'

    # Si hay una diferencia escribirla
    if diacnostic_str != '':
        # Escribir en el archivo las línes que existen en un archivo y en el otro no
        with open('./output/diagnostic_p&id.txt', mode='a') as f:
            f.write(diacnostic_str)


def valves_diferences(bom_lines_unique, pid_lines_unique, mto_df, pid_df):
    # Hacer una copia de los dataframes
    mto_df = mto_df.copy()
    pid_df = pid_df.copy()

    # Sacar únicamente las válvulas del MTO
    mto_df = mto_df[(mto_df['TYPE']) == 'VL']

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
                                     'FIRST_SIZE_NUMBER', 'RATING', 'QTY']].apply(common_index, axis=1)

    pid_df['common_index'] = pid_df[['LINE_NUM', 'SPEC', 'TYPE_CODE',
                                     'FIRST_SIZE_NUMBER', 'RATING', 'QTY']].apply(common_index, axis=1)

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
                        'RATING_x', 'QTY_x']]

        mto_df.rename(columns={'LINE_NUM_x': 'LINE_NUM', 'SPEC_x': 'SPEC', 'TYPE_CODE_x': 'TYPE_CODE', 'FIRST_SIZE_NUMBER_x': 'FIRST_SIZE_NUMBER',
                               'RATING_x': 'RATING', 'QTY_x': 'QTY'}, inplace=True)

        # Redefinir P&ID
        pid_df = merge_df[merge_df['LINE_NUM_x'].isnull()]

        pid_df = pid_df[['LINE_NUM_y', 'SPEC_y', 'TYPE_CODE_y', 'FIRST_SIZE_NUMBER_y',
                        'RATING_y', 'QTY_y']]

        pid_df.rename(columns={'LINE_NUM_y': 'LINE_NUM', 'SPEC_y': 'SPEC', 'TYPE_CODE_y': 'TYPE_CODE', 'FIRST_SIZE_NUMBER_y': 'FIRST_SIZE_NUMBER',
                               'RATING_y': 'RATING', 'QTY_y': 'QTY'}, inplace=True)

        # Crer un índice para comparar si hay hay diferencias en cantidades y ratings
        mto_df['common_index'] = mto_df[['LINE_NUM', 'SPEC', 'TYPE_CODE',
                                        'FIRST_SIZE_NUMBER']].apply(common_index_2, axis=1)

        pid_df['common_index'] = pid_df[['LINE_NUM', 'SPEC', 'TYPE_CODE',
                                        'FIRST_SIZE_NUMBER']].apply(common_index_2, axis=1)

        # Hacer el nuevo merge
        merge_df = pd.merge(mto_df, pid_df, how='outer', on='common_index')

        # Saber si se imprime el archivo temporales o no
        if merge_df.shape[0] > 0:
            # Hacer un diagnóstico sobre cada una de las válvulas
            merge_df['common_index'] = merge_df[['LINE_NUM_x', 'SPEC_x', 'TYPE_CODE_x', 'FIRST_SIZE_NUMBER_x',
                                                'RATING_x', 'QTY_x', 'LINE_NUM_y', 'SPEC_y',
                                                 'TYPE_CODE_y', 'FIRST_SIZE_NUMBER_y', 'RATING_y', 'QTY_y']].apply(diacnostic, axis=1, pid_lines_unique=pid_lines_unique, bom_lines_unique=bom_lines_unique)

            print(
                '❌  HAY DIFERENCIAS ENTRE LAS VÁLVULAS REPORTADAS POR EL B.O.M Y EL P&ID\n')

            merge_df.to_csv('./output/p&id_temp.csv')
        else:
            print(
                '✅  NO HAY DIFERENCIAS ENTRE LAS VÁLVULAS REPORTADAS POR EL B.O.M Y EL P&ID\n')
