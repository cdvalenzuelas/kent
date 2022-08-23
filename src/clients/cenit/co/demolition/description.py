import re

# (VALEC17) Definir la descripción de la demolición en función del tipo de elemento


def def_demolition_description(row, method):
    line, type_element, demolition_description, weight, underground, forgiven = row

    if type_element == 'VL':

        if weight <= 200:
            return 'DESMANTELAMIENTO DE VÁLVULAS CUYO PESO SEA ≤ 200 KG(INCLUYE TRANSPORTE Y DISPOSICIÓN FINAL)'
        elif weight > 200 and weight <= 500:
            return 'DESMANTELAMIENTO DE VÁLVULA CUYO PESO SEA > 200 KG HASTA 500 KG (INCLUYE TRANSPORTE Y DISPOSICIÓN FINAL)'
        elif weight > 500 and weight <= 1000:
            return 'DESMANTELAMIENTO DE VÁLVULA CUYO PESO SEA > 500 KG HASTA 1.000 KG (INCLUYE TRANSPORTE Y DISPOSICIÓN FINAL)'
        elif weight > 1000 and weight <= 3000:
            return 'DESMANTELAMIENTO DE VÁLVULA CUYO PESO SEA ENTRE 1.001 KG HASTA 3.000 KG (INCLUYE TRANSPORTE Y DISPOSICIÓN FINAL)'
        elif weight > 3000 and weight <= 6000:
            return 'DESMANTELAMIENTO DE VÁLVULA CUYO PESO SEA ENTRE 3.001 KG HASTA 6.000 KG (INCLUYE TRANSPORTE Y DISPOSICIÓN FINAL)'
        else:
            return 'DESMANTELAMIENTO DE VÁLVULA CUYO PESO SEA > 6.000 KG (INCLUYE TRANSPORTE Y DISPOSICIÓN FINAL)'
    else:
        # (VALEC17) Si el desmantelamiento se ará con oxicorte se debe modificar la descripción
        if method == 'hot':
            demolition_description = re.sub(
                'CORTE EN FRÍO', 'OXICORTE', demolition_description)

        # (VALEC17)
        if underground:
            demolition_description = re.sub(
                'AÉREAS', 'ENTERRADAS', demolition_description)

        if forgiven:
            demolition_description = 'ABANDONO TECNICO DE TUBERIA ENTERRADA'

    return demolition_description
