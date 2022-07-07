import re


# Crea una columna comun entre el mto y los bolt
def concat_bolt_index(row):
    first_size, rating, face = row

    rating = str(rating)

    rating = re.sub('[.]0', '', rating)

    return f'{first_size} {rating} {face}'


# Definir el Diámetro de los pernos
def bolts_diameter(row):
    diameter, type_code, first_size = row

    if type_code == 'BOLT':
        return diameter
    else:
        return first_size


# Definir el Diámetro de los pernos
def bolts_diameter_number(row):
    diameter, type_code, first_size_number = row

    if type_code == 'BOLT':
        return diameter
    else:
        return first_size_number


# Definir longitudes de los pernos
def bolts_length(row):
    length, type_code, second_size = row

    if type_code == 'BOLT':
        return f'{int(length)}mm'
    else:
        return second_size


# Definir longitudes de los pernos
def bolts_length_number(row):
    length, type_code, second_size_number = row

    if type_code == 'BOLT':
        return f'{int(length)}mm'
    else:
        return second_size_number


# Borrar ratings de bolts
def delete_bolts_rating(row):
    code_type, rating = row

    if code_type == 'BOLT':
        return '-'
    else:
        return rating


# Borrar face de bolts
def delete_bolts_face(row):
    code_type, face = row

    if code_type == 'BOLT':
        return '-'
    else:
        return face


# Definir el tamaño de los pernos
def bolts_weight(row):
    type_code, weight, bolt_weight = row

    if type_code == 'BOLT':
        return bolt_weight
    else:
        return weight
