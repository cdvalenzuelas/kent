def description(mto_diagnostic_2, short_desc_2, short_description_2, short_desc):
    # (VALEC17) DESCRIPTION Diagnostic
    if short_desc_2 != short_description_2:
        return mto_diagnostic_2 + f'* La DESCRIPTION no coincide, en el BOM es "{short_desc}" y en el piping_class es "{short_desc}". Se deben revisar los isométricos\n'
    else:
        return mto_diagnostic_2
