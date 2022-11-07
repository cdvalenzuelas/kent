def wafer_bolts(item, line_num, first_size, type_code):
    # (VALEC17) Verificar longitudes de pernos si existe un equipo tipo wafer
    if type_code == 'F8':
        mto_diagnostic = f"""ITEM {item}: {line_num} , {type_code}, {first_size}
---------------------------------------------
* Existe una figura en 8. Modificar el tag de lo pernos para modificar su longitud.

"""

        with open('./diacnostic/3.difference_design.txt', mode='a') as f:
            f.write(mto_diagnostic)

    elif type_code == 'BTY':
        mto_diagnostic = f"""ITEM {item}: {line_num} , {type_code}, {first_size}
---------------------------------------------
* Existe una válvula de mariposa. Modificar el tag de lo pernos para modificar su longitud.

"""
        with open('./diacnostic/3.difference_design.txt', mode='a') as f:
            f.write(mto_diagnostic)
