def bolt_length(mto_diagnostic, type_code, length):
    # Ver diferencias en longitudes de pernos
    if type_code == 'BOLT' and length != bolt_length:
        return mto_diagnostic + f'* La longitud de los pernos no coincide, en el BOM es de {length}mm y en el piping_class es de {bolt_length}mm. Se deben revisar los isométricos \n'
    else:
        return mto_diagnostic