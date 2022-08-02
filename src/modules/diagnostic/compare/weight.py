# PESOS UNITARIOS diqagnostic (Evidenciar una variación mayor al 5% del peso verdadero)
def weight(mto_diagnostic_2, type_code, weight_x, weight_y, bolt_weight, qty, length, diagnostic_dict):
    if type_code in ['PE', 'BE', 'TE']:
        length = float(length)
        if 1000*weight_x/length >= 1.05*float(weight_y) or 1000*weight_x/length <= 0.95*float(weight_y):
            diagnostic_dict['weight_spec'].append(1000*weight_x/length)
            diagnostic_dict['weight_piping'].append(weight_y)

            return (mto_diagnostic_2 + f'* El WEIGHT_PER_UNIT no coincide, en el BOM es {1000*weight_x/length}kg ({weight_x}kg totales) y en el piping_class es {weight_y*length/1000}kg ({weight_y*qty}kg totales). Se deben revisar los isométricos \n', diagnostic_dict)
    elif type_code == 'BOLT':
        qty = float(qty)
        if weight_x/qty >= 1.05*float(bolt_weight) or weight_x/qty <= 0.95*float(bolt_weight):
            diagnostic_dict['weight_spec'].append(weight_x/qty)
            diagnostic_dict['weight_piping'].append(bolt_weight)

            if weight_y > 0:
                return (mto_diagnostic_2 + f'* El WEIGHT_PER_UNIT no coincide, en el BOM es {weight_x/qty}kg ({weight_x}kg totales) y en el piping_class es {weight_y}kg ({weight_y*qty}kg totales). Se deben revisar los isométricos \n', diagnostic_dict)
    else:
        qty = float(qty)
        if weight_x/qty >= 1.05*float(weight_y) or weight_x/qty <= 0.95*float(weight_y):
            diagnostic_dict['weight_spec'].append(weight_x/qty)
            diagnostic_dict['weight_piping'].append(weight_y)

            if weight_y > 0:
                return (mto_diagnostic_2 + f'* El WEIGHT_PER_UNIT no coincide, en el BOM es {weight_x}kg ({weight_x*qty}kg totales) y en el piping_class es {weight_y}kg ({weight_y*qty}kg totales). Se deben revisar los isométricos \n', diagnostic_dict)

    diagnostic_dict['weight_spec'].append(None)
    diagnostic_dict['weight_piping'].append(None)

    return (mto_diagnostic_2, diagnostic_dict)
