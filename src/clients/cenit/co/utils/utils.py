from src.utils.normalize_string import normalize_string


# (VALEC17) Crea un índice común entre la plantilla y las cantidades de obra calculadas
def common_index(description):
    # (VALEC17) Normalizar index. Pasa las cosas a mayúsculas, eliminar comillas, puntos, comas, punto y comas, tildes, guiones y espacio
    index = normalize_string(description)

    return index


# (VALEC17) Definde si un elemento no se encuentra en la plantilla (para el supply)
def def_note(row):
    area, note = row

    if area == '-':
        return 'NUEVO'

    if note == 'NUEVO':
        return 'NUEVO'


# (VALEC17) Define la descripción de los elementos nuevos
def def_description(row):
    description, supply_description = row

    if description == '-':
        return supply_description
    else:
        return description


# (VALEC17) Define la cantidad de los elementos nuevos
def def_qty(row):
    qty_x, qty_y = row

    if qty_y == '-' and qty_x == '-':
        return 0

    if qty_y == '-':
        return qty_x

    if qty_x == '-':
        return qty_y

    if qty_x == 0:
        return qty_y


# (VALEC17) Define las unidades de los elementos nuevos
def def_units(row):
    type_code, unit = row

    if type_code == '-':
        return unit
    else:
        if type_code in ['PE', 'BE', 'TE']:
            return 'M'
        else:
            return 'UN'
