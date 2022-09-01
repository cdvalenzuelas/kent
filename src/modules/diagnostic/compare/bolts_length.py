def bolt_length(mto_diagnostic, type_code, length, bolt_length_piping, diagnostic_dict):
    # (VALEC17) Ver diferencias en longitudes de pernos
    if type_code == 'BOLT':

        # (VALEC17) Si la longitud de pernos es distinta en la extracción y en el piping class generar reporte
        if length != bolt_length_piping:

            diagnostic_dict['bolt_length_spec'].append(length)
            diagnostic_dict['bolt_length_piping'].append(bolt_length_piping)

            return (mto_diagnostic + f'* La longitud de los pernos no coincide, en el BOM es de {length}mm y en el piping_class es de {bolt_length_piping}mm. Se deben revisar los isométricos \n', diagnostic_dict)
        # (VALEC17) Si la longitud es igual en las dos partes no generar reporte
        else:
            diagnostic_dict['bolt_length_spec'].append(None)
            diagnostic_dict['bolt_length_piping'].append(None)

            return (mto_diagnostic, diagnostic_dict)

    diagnostic_dict['bolt_length_spec'].append(None)
    diagnostic_dict['bolt_length_piping'].append(None)

    return (mto_diagnostic, diagnostic_dict)
