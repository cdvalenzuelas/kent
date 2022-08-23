def quantity_and_rating_diferences(row):
    line_x, type_x, size_x, spec_x, qty_x, qty_y, rating_x, rating_y = row

    # (VALEC17) Pasar los parámetros de comparación a strings y eliminar lo ',00'
    size_x = str(size_x).replace(',00', '')
    rating_x = str(rating_x).replace(',00', '')
    rating_y = str(rating_y).replace(',00', '')

    rating_diff = ''
    qty_diff = ''
    diacnostic_str = ''

    # (VALEC17) Ver diferencias en ratings
    if rating_x != rating_y:
        rating_diff = f"""
El rating no correspone, en el P&ID es {rating_y} pero por piping_class debería ser {rating_x}, se debe evaluar el P&ID (hablar con procesos)."""

    # (VALEC17) Ver diferencias en cantidades
    if qty_x != qty_y:
        compare = 'más' if qty_x > qty_y else 'menos'
        qty_diff = f"""
Las cantidades no coinciden, en el B.O.M es {qty_x} y en P&ID es {qty_y}. Existen {compare} válvulas en la maqueta que en el P&ID."""

    # (VALEC17) Ver si existen diferencias en ratings o diferencias en cantidades
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

            # (VALEC17) Escribir el archivo de diagnóstico
        with open('./output/diagnostic_p&id.txt', mode='a') as f:
            f.write(diacnostic_str)

        return 'difference'

    else:
        return 'no_difference'
