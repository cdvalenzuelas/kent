import re


# (VALEC17) Crea una columna comun entre el mto y los bolt
def concat_bolt_index(row):
    type_code, first_size, rating, face, tag = row

    rating = str(rating)

    rating = re.sub('[.]0', '', rating)

    return f'{type_code} {first_size} {rating} {face} {tag}'


# (VALEC17) Definir el Diámetro de los pernos
def bolts_diameter(row):
    diameter, type_code, first_size = row

    if type_code == 'BOLT':
        return diameter
    else:
        return first_size


# (VALEC17) Definir el Diámetro de los pernos
def bolts_diameter_number(row):
    diameter, type_code, first_size_number = row

    if type_code == 'BOLT':
        return diameter
    else:
        return first_size_number


# (VALEC17) Definir longitudes de los pernos
def bolts_length(row):
    length, type_code, second_size = row

    if type_code == 'BOLT':
        return f'{int(length)}mm'
    else:
        return second_size


# (VALEC17) Definir longitudes de los pernos
def bolts_length_number(row):
    length, type_code, second_size_number = row

    if type_code == 'BOLT':
        return f'{int(length)}mm'
    else:
        return second_size_number


# (VALEC17) Borrar ratings de bolts
def delete_bolts_rating(row):
    code_type, rating = row

    if code_type == 'BOLT':
        return '-'
    else:
        return rating


# (VALEC17) Borrar face de bolts
def delete_bolts_face(row):
    code_type, face = row

    if code_type == 'BOLT':
        return '-'
    else:
        return face


# (VALEC17) Definir el tamaño de los pernos
def bolts_weight(row):
    type_code, weight, bolt_weight = row

    if type_code == 'BOLT':
        return bolt_weight
    else:
        return weight
