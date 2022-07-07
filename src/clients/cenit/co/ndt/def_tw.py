# Definir la cantidad de soldaduras TW
def def_tw(row):
    face, type_code, diametric_welds, first_size_number, second_size_number, qty = row

    first_size_number = float(first_size_number)
    second_size_number = float(second_size_number)

    if type_code in ['SOL', 'WOL', 'LOL', 'THD']:
        return second_size_number*qty

    return 0
