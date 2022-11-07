def description(short_desc_2, short_description_2, short_desc, short_description, diagnostic_dict):
    # (VALEC17) DESCRIPTION Diagnostic
    if short_desc_2 != short_description_2:
        diagnostic_dict['description_spec'].append(short_desc)
        diagnostic_dict['description_piping'].append(short_description)
        return diagnostic_dict
    else:
        diagnostic_dict['description_spec'].append(None)
        diagnostic_dict['description_piping'].append(None)
        return diagnostic_dict
