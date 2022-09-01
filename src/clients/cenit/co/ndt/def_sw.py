# (VALEC17) Definir la cantidad de soldaduras SW
def def_sw(row):
    face, type_code, diametric_welds, first_size_number, second_size_number, qty = row

    first_size_number = float(first_size_number)
    second_size_number = float(second_size_number)

    if face in ['PE', 'SW']:
        return diametric_welds

    if type_code in ['SW']:
        return diametric_welds

    if type_code in ['SWC', 'SWE']:
        if face in ['BExPE', 'BWxPE', 'TExPE', 'THDxPE', 'BExSW', 'BWxSW', 'TExSW', 'THDxSW']:
            return second_size_number * qty

    return 0
