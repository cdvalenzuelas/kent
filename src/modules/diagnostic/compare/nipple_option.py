def nipple_option(mto_diagnostic, type_code, length):
    # Ver si alguna tubería se puede sustituir con un niple
    if type_code in ['PE', 'BE', 'TE'] and float(length) <= 200:
        return mto_diagnostic + f'* La longitud de la tubería es muy corta ({length}mm), podría ser un niple. Revisar si se puede cambiar \n'
    else:
        return mto_diagnostic
