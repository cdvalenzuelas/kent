def nipple_option(item, line_num, type_code, first_size, length):
    # (VALEC17) Ver si alguna tubería se puede sustituir con un niple
    if type_code in ['PE', 'BE', 'TE'] and float(length) <= 200:
        # (VALEC17) Escribir en el archivo de cosas importantes
        mto_diagnostic = f"""ITEM {item}: {line_num} , {type_code}, {first_size}
---------------------------------------------
* La longitud de la tubería es muy corta ({length}mm), podría ser un niple. Revisar si se puede cambiar

"""

        with open('./diacnostic/3.difference_design.txt', mode='a') as f:
            f.write(mto_diagnostic)
