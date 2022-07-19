import re


def def_erection_description(row):
    description, underground, premanufacturing = row

    match = re.search(
        r'^(MONTAJE AÉREO DE TUBERÍA DE Ø)[\s]+[<]?[\s]?([-0-9/]+)["]$', description)

    if match:
        size = f'{match.groups()[1]}"' if '<' not in description else f'< {match.groups()[1]}"'

        if underground and premanufacturing:
            return f'MONTAJE ENTERRADO DE TUBERÍA DE Ø {size}'
        elif underground:
            return f'MONTAJE ENTERRADO DE TUBERÍA DE Ø {size} (SIN PREFABRICAR)'
        elif premanufacturing:
            return f'MONTAJE AÉREO DE TUBERÍA DE Ø {size}'
        else:
            return f'MONTAJE AÉREO DE TUBERÍA DE Ø {size} (SIN PREFABRICAR)'

    return description
