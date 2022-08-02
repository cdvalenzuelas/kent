def bolt_length(mto_diagnostic, type_code, length, bolt_length_piping, diagnostic_dict):
    # Ver diferencias en longitudes de pernos
    if type_code == 'BOLT' and length != bolt_length_piping:
        diagnostic_dict['bolt_length_spec'].append(length)
        diagnostic_dict['bolt_length_piping'].append(bolt_length_piping)

        return (mto_diagnostic + f'* La longitud de los pernos no coincide, en el BOM es de {length}mm y en el piping_class es de {bolt_length_piping}mm. Se deben revisar los isométricos \n', diagnostic_dict)
    else:
        diagnostic_dict['bolt_length_spec'].append(None)
        diagnostic_dict['bolt_length_piping'].append(None)

        return (mto_diagnostic, diagnostic_dict)
