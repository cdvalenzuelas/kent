def def_main_size(row):
    type_code, size = row

    if type_code == 'BOLT':
        return '-'

    main_size = size.upper().replace(' ', '').split('X')[
        0].replace('+', '-') + '"'

    return main_size
