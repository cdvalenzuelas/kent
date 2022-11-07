def no_bom_valves(row):
    line_y, qty_y, type_y, size_y, rating_y, spec_y = row

    # (VALEC17) Pasar los parámetros de comparación a strings y eliminar lo ',00'
    size_y = str(size_y).replace(',00', '')
    rating_y = str(rating_y).replace(',00', '')

    diacnostic_str = f"""
La línea {line_y} contiene {qty_y} válvulas de tipo {type_y}, diámetro {size_y}", rating {rating_y} y spec {spec_y}.
Éstas válvulas existen en el P&ID pero no en el B.O.M. Es posible que éstas válvulas no se encuentren ruteadas o que
las líneas estén mal nombradas en la maqueta.
        """

    # (VALEC17) Escribir el archivo de diagnóstico
    with open('./diacnostic/lines_difference.txt', mode='a') as f:
        f.write(diacnostic_str)

    return 'difference'
