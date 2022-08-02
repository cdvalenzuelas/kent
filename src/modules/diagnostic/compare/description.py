def description(mto_diagnostic_2, short_desc_2, short_description_2, short_desc, diagnostic_dict):
    # DESCRIPTION Diagnostic
    if short_desc_2 != short_description_2:
        diagnostic_dict['description_spec'].append(short_desc)
        diagnostic_dict['description_piping'].append(short_desc_2)
        return (mto_diagnostic_2 + f'* La DESCRIPTION no coincide, en el BOM es "{short_desc}" y en el piping_class es "{short_desc_2}". Se deben revisar los isométricos\n', diagnostic_dict)
    else:
        diagnostic_dict['description_spec'].append(None)
        diagnostic_dict['description_piping'].append(None)
        return (mto_diagnostic_2, diagnostic_dict)
