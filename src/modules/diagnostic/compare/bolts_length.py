def bolt_length(type_code, length, bolt_length_piping, diagnostic_dict):
    # (VALEC17) Ver diferencias en longitudes de pernos
    if type_code == 'BOLT':

        # (VALEC17) Si la longitud de pernos es distinta en la extracción y en el piping class generar reporte
        if length != bolt_length_piping:

            diagnostic_dict['bolt_length_spec'].append(length)
            diagnostic_dict['bolt_length_piping'].append(bolt_length_piping)

            return diagnostic_dict
        # (VALEC17) Si la longitud es igual en las dos partes no generar reporte
        else:
            diagnostic_dict['bolt_length_spec'].append(None)
            diagnostic_dict['bolt_length_piping'].append(None)

            return diagnostic_dict

    diagnostic_dict['bolt_length_spec'].append(None)
    diagnostic_dict['bolt_length_piping'].append(None)

    return diagnostic_dict
