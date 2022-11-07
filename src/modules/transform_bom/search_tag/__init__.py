def find_tag(row, piping_class):
    spec, type_code, first_size, second_size, description, tag = row

    description = description.upper()

    # (VALEC17) TAGS PARA LOS PERNOS
    if type_code == 'BOLT' and tag in ['-', 'F8', 'BTY']:
        return tag
    elif type_code == 'BOLT' and tag not in ['-', 'F8', 'BTY']:
        return 'ERROR'

    # (VALEC17) SI SON NIPLES O COUPLIGS TIENEN SU TAG EN SU FACE
    if type_code in ['NIP', 'CPL'] and tag not in ['PExTE', 'SWxTHD', 'BExTE', 'PE', 'TE', 'SW', 'THD']:
        if ' PEXTE,' in description or ' PEXTE' in description or '/PEXTE' in description:
            return 'PExTE'
        elif ' SWXTHD,' in description or ' SWXTHD' in description or '/SWXTHD' in description:
            return 'SWxTHD'
        elif ' BEXTE,' in description or ' BEXTE' in description or '/BEXTE' in description or 'NPTM END/BE' in description:
            return 'BExTE'
        elif ' PE,' in description or ' PE' in description or '/PE' in description:
            return 'PE'
        elif ' TE,' in description or ' TE' in description or '/TE' in description:
            return 'TE'
        elif ' SW,' in description or ' SW' in description or '/SW' in description:
            return 'SW'
        elif ' THD,' in description or ' THD' in description or '/THD' in description:
            return 'THD'
    elif type_code in ['NIP', 'CPL'] and tag in ['PExTE', 'SWxTHD', 'BExTE', 'PE', 'TE', 'SW', 'THD']:
        return tag

    # (VALEC17) Detectar los elementos que cumplen con el type_code, spec y diámetros
    sub_piping_class = piping_class[(
        piping_class['TYPE_CODE'] == type_code) &
        (piping_class['SPEC'] == spec) &
        (piping_class['FIRST_SIZE'] == first_size) &
        (piping_class['SECOND_SIZE'] == second_size)]

    # (VALEC17) TAGS ENCONTRADOS
    tags = sub_piping_class.loc[:, 'TAG'].tolist()

    # (VALEC17) Determinar cuantos elementos cuentan con las características anteriores
    shape = sub_piping_class.shape[0]

    # (VALEC17) Si sólo hay un elemento que le ponga el tag correspondiente
    if shape == 1:
        return tags[0]
    # (VALEC17) Si no se encuentra el elemento retornar '-'
    elif shape == 0:
        return '-'
    # (VALEC17) SI HAY MÁS DE UN TAG POR ELEMENTO
    else:
        # (VALEC17) SI EL USUARIO YA CORRIGIÓ EL TAG NO MODIFICARLO
        if tag in tags:
            return tag

        return '-'


def search_tag(bom_df, piping_class):
    # (VALEC17) Hacer una copia del piping class
    piping_class = piping_class.copy()
    bom_df = bom_df.copy()

    bom_df['TAG'] = bom_df[['SPEC_FILE', 'DB_CODE', 'MAIN_NOM', 'RED_NOM', 'SHORT_DESC', 'TAG']].apply(
        find_tag, axis=1, piping_class=piping_class)

    return bom_df
