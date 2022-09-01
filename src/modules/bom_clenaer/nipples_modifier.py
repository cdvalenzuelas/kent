# (VALEC17) Definir la longitud de los niples como segunda longitud
def nipple_second_size(row):
    length, db_code, red_nom = row

    if db_code == 'NIP':
        length = float(length)
        return f'{int(length)}mm'
    else:
        return red_nom


# (VALEC17) Definir la longitud de los niples como segunda longitud
def nipple_second_size_number(row):
    length, db_code, red_nom = row

    if db_code == 'NIP':
        length = float(length)
        return f'{int(length)}mm'
    else:
        return red_nom
