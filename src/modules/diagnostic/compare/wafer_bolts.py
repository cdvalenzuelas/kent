def wafer_bolts(mto_diagnostic, type_code):
    # Verificar longitudes de pernos si existe un equipo tipo wafer
    if type_code in ['F8', 'BTY']:
        return mto_diagnostic + f'* Este es un equipo tipo wafer vefificar pernos.\n'
    else:
        return mto_diagnostic
