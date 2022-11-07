import re

# (VALEC17) DEFINIR LA LONGITUD DE LOS ELEMENTOS


def def_lenght(row):
    type_code, qty, first_size, second_size, description = row

    lenght = 0

    # (VALEC17) DEFINIR LONGITUD DE TUBERÍAS
    if type_code in ['PE', 'BE', 'TE']:
        lenght = str(qty).replace('.', '')

        return float(lenght)
    # (VALEC17) DEFINIR LONGITUD DE NIPLES
    elif type_code == 'NIP':
        try:
            lenght = re.match(
                '.+L\s+=\s+([0-9]+)mm.+', description).groups()[0]
            return float(lenght)
        except:
            return lenght
    # (VALEC17) DEFINIR LA LONGITUD DE LOS PERNOS
    # ^[A-Za-z\s,0-9.\/]{1,}L=([0-9]{1,})mm$
    elif type_code == 'BOLT':
        # (VALEC17) SI LA LONGITUD DE LOS PERNOS ESTÁ EN LA DESCRIPCIÓN EXTRAERLA
        return float(second_size)

    # (VALEC17) EN CASO DE QUE NO SEAN NIPLES, TUBERÍAS O PERNOS
    return '-'
