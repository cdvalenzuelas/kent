# (VALEC17) Hacer un diagnótico sobre cada válvula
def diacnostic(row, pid_lines_unique, bom_lines_unique):
    line_x, spec_x, type_x, size_x, rating_x, qty_x, line_y, spec_y, type_y, size_y, rating_y, qty_y = row

    # (VALEC17) Pasar los parámetros de comparación a strings y eliminar lo ',00'
    size_x = str(size_x).replace(',00', '')
    size_y = str(size_y).replace(',00', '')
    rating_x = str(rating_x).replace(',00', '')
    rating_y = str(rating_y).replace(',00', '')

    diacnostic_str = ''

    if str(line_y) == 'nan' and line_x not in bom_lines_unique:
        diacnostic_str = f"""
La línea {line_x} contiene {qty_x} válvulas de typo {type_x}, diámetro {size_x}", rating {rating_x}, y spec {spec_x}.
Éstas válvulas existen en el B.O.M pero no en el P&ID. Contrastar la maqueta con el P&ID. Es posible que la línea esté
mal nombrada en la maqueta, esté mal seleccionado el tipo de válvula, el diámetro, el rating o el spec con respecto al P&ID. 
        """

    if str(line_x) == 'nan' and line_y not in pid_lines_unique:
        diacnostic_str = f"""
La línea {line_y} contiene {qty_y} válvulas de tipo {type_y}, diámetro {size_y}", rating {rating_y} y spec {spec_y}.
Éstas válvulas existen en el P&ID pero no en el B.O.M. Es posible que éstas válvulas no se encuentren ruteadas o que
las líneas estén mal nombradas en la maqueta.
        """

    # (VALEC17) Establecer diferencias ratings y cantidades (los tags ya vienen solucionados desde antes)
    if str(line_x) != 'nan' and str(line_y) != 'nan':

        rating_diff = ''
        qty_diff = ''

        # (VALEC17) Ver diferencias en ratings
        if rating_x != rating_y:
            rating_diff = f"""
El rating no correspone, en el P&ID es {rating_y} pero por piping_class debería ser {rating_x}, se debe evaluar el P&ID (hablar con procesos)."""

        # (VALEC17) Ver diferencias en cantidades
        if qty_x != qty_y:
            compare = 'más' if qty_x > qty_y else 'menos'
            qty_diff = f"""
Las cantidades no coinciden, en el B.O.M es {qty_x} y en P&ID es {qty_y}. Existen {compare} válvulas en la maqueta que en el P&ID."""

        if rating_diff != '' or qty_diff != '':
            diacnostic_str = f"""
La línea {line_x} contiene válvulas de tipo {type_x}, diámetro {size_x}" y spec {spec_x}.
Las válvulas mensionadas anteriormente tienen diferencias en rating o cantidades."""

        if rating_diff and qty_diff:
            diacnostic_str = diacnostic_str + rating_diff + qty_diff + '\n'
        elif rating_diff:
            diacnostic_str = diacnostic_str + rating_diff + '\n'
        elif qty_diff:
            diacnostic_str = diacnostic_str + qty_diff + '\n'

    # (VALEC17) Si hay una diferencia escribirla
    if diacnostic_str != '':
        # (VALEC17) Escribir en el archivo las línes que existen en un archivo y en el otro no
        with open('./output/diagnostic_p&id.txt', mode='a') as f:
            f.write(diacnostic_str)

        return 'difference'
    else:
        return 'no_difference'
