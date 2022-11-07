import re

# (VALEC17) DEFINIR LA LONGITUD DE LOS ELEMENTOS


def def_lenght(row):
    type_code, qty, size, description = row

    lenght = 0

    # (VALEC17) DEFINIR LONGITUD DE TUBERÍAS
    if type_code in ['PE', 'BE', 'TE']:
        lenght = str(qty).replace(' m', '')
        lenght = float(lenght)*1000

        return lenght
    # (VALEC17) DEFINIR LONGITUD DE NIPLES
    elif type_code == 'NIP':
        lenght = size.upper().replace(' ', '').split('X')[1].replace('M', '')
        lenght = float(lenght)*1000

        return lenght
    # (VALEC17) DEFINIR LA LONGITUD DE LOS PERNOS
    # ^[A-Za-z\s,0-9.\/]{1,}L=([0-9]{1,})mm$
    elif type_code == 'BOLT':
        # (VALEC17) SI LA LONGITUD DE LOS PERNOS ESTÁ EN LA DESCRIPCIÓN EXTRAERLA
        try:
            lenght = re.match(
                '.+L\s+=\s+([0-9]+)mm.+', description).groups()[0]
            lenght = float(lenght)

            return lenght
        # (VALEC17) SI LA LONGITUD DE LOS PERNOS NO ESTÁ EN LA DESCRIPCIÓN EXTRAERLA DEL SIZE
        except:
            lenght = size.upper().replace(' ', '').split('X')[
                1].replace('M', '')
            lenght = float(lenght)*1000

            return lenght

    # (VALEC17) EN CASO DE QUE NO SEAN NIPLES, TUBERÍAS O PERNOS
    return '-'
