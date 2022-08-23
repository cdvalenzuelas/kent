def no_pid_valves(row):
    line_x, qty_x, type_x, size_x, rating_x, spec_x = row

    # (VALEC17) Pasar los parámetros de comparación a strings y eliminar lo ',00'
    size_x = str(size_x).replace(',00', '')
    rating_x = str(rating_x).replace(',00', '')

    diacnostic_str = f"""
La línea {line_x} contiene {qty_x} válvulas de typo {type_x}, diámetro {size_x}", rating {rating_x}, y spec {spec_x}.
Éstas válvulas existen en el B.O.M pero no en el P&ID. Contrastar la maqueta con el P&ID. Es posible que la línea esté
mal nombrada en la maqueta, esté mal seleccionado el tipo de válvula, el diámetro, el rating o el spec con respecto al P&ID. 
        """

    # (VALEC17) Escribir el archivo de diagnóstico
    with open('./output/diagnostic_p&id.txt', mode='a') as f:
        f.write(diacnostic_str)

    return 'difference'
