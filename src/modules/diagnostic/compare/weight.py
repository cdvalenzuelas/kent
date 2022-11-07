# (VALEC17) PESOS UNITARIOS diqagnostic (Evidenciar una variación mayor al 5% del peso verdadero)
def weight(type_code, weight_x, weight_y, bolt_weight, qty, length, diagnostic_dict):

    # (VALEC17) VER SI SE TRATA DE TUBERÍAS Y HAY UNA DIFERENCIA DE MÁS O MENOS 5% EN PESO
    if type_code in ['PE', 'BE', 'TE']:
        length = float(length)
        if 1000*weight_x/length >= 1.05*float(weight_y) or 1000*weight_x/length <= 0.95*float(weight_y):
            diagnostic_dict['weight_spec'].append(1000*weight_x/length)
            diagnostic_dict['weight_piping'].append(weight_y)

            return diagnostic_dict

    # (VALEC17) VER SI SON PERNOS Y HAY UNA DIFERENCIA DE MÁS O MENOS 5% EN PESO
    if type_code == 'BOLT':
        qty = float(qty)
        if weight_x/qty >= 1.05*float(bolt_weight) or weight_x/qty <= 0.95*float(bolt_weight):
            diagnostic_dict['weight_spec'].append(weight_x/qty)
            diagnostic_dict['weight_piping'].append(bolt_weight)

            return diagnostic_dict

    # (VALEC17) SI NO SE TRATA DE PERNO NI TUBERÍAS PERO HAY DIFERENCIA EN PESOS
    qty = float(qty)
    weight_y = float(weight_y)
    weight_x = float(weight_x)

    if weight_x/qty >= 1.05*float(weight_y) or weight_x/qty <= 0.95*float(weight_y):
        diagnostic_dict['weight_spec'].append(weight_x/qty)
        diagnostic_dict['weight_piping'].append(weight_y)

        return diagnostic_dict

    # (VALEC17) SI LOS PESOS ESTÁN BIEN NO GENERAR NADA NEGATIVO
    diagnostic_dict['weight_spec'].append(None)
    diagnostic_dict['weight_piping'].append(None)

    return diagnostic_dict
