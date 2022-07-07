# Definir la cantidad de soldaduras BW
def def_bw(row):
    face, type_code, diametric_welds, first_size_number, second_size_number, qty = row

    first_size_number = float(first_size_number)
    second_size_number = float(second_size_number)

    if face in ['BE', 'BW']:
        return diametric_welds

    if type_code in ['WNK', 'ORF']:
        return diametric_welds

    if type_code in ['SWC', 'SWE']:
        if face in ['BExPE', 'BWxPE', 'BExTE', 'BWxTE', 'BExTHD', 'BWxTHD']:
            return first_size_number * qty

    return 0
