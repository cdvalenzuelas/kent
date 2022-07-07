# Calcular las soldaduras por cada elementos
def welds_per_element(row):
    type_element, type_code, first_size_number, second_size_number, qty, face = row

    first_size_number = float(first_size_number)
    second_size_number = float(second_size_number)

    if type_code in ['WNK', 'SW', 'CAP', 'LAP', 'ORF']:
        return first_size_number*qty

    if type_code in ['SOL', 'WOL', 'LOL']:
        return second_size_number * qty

    if type_code in ['90L', '45L', 'CPL', 'UNN', 'SLP']:
        return 2*first_size_number*qty

    if type_code in ['TEE']:
        return 3*first_size_number*qty

    if type_code in ['CRE', 'ERE']:
        return (first_size_number + second_size_number)*qty

    if type_code in ['RTE']:
        return (2*first_size_number + second_size_number)*qty

    if type_code in ['SWC', 'SWE']:
        # OJO DEPENDE DEL FACE
        return (first_size_number + second_size_number)*qty

    if type_code in ['PE', 'BE']:
        int_division = int(qty/6)

        if qty/6 > int_division:
            return int_division
        else:
            if int_division == 0:
                return 0
            else:
                return int_division - 1

    if type_code in ['NIP', 'TE', 'TOL', 'BLD', 'THD']:
        return 0
