# Definir la longitud de los niples como segunda longitud
def nipple_second_size(row):
    length, db_code, red_nom = row

    if db_code == 'NIP':
        return f'{int(length)}mm'
    else:
        return red_nom


# Definir la longitud de los niples como segunda longitud
def nipple_second_size_number(row):
    length, db_code, red_nom = row

    if db_code == 'NIP':
        return f'{int(length)}mm'
    else:
        return red_nom
