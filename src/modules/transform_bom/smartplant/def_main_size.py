def def_main_size(row):
    type_code, first_size = row

    if str(first_size) == '0.5':
        return '1/2"'
    elif str(first_size) == '0.625':
        return '5/8"'
    elif str(first_size) == '0.75':
        return '3/4"'
    elif str(first_size) == '0.875':
        return '7/8"'
    elif str(first_size) == '1.125':
        return '1-1/8"'
    elif str(first_size) == '1.25':
        return '1-1/4"'
    elif str(first_size) == '1.375':
        return '1-3/8"'
    elif str(first_size) == '1.5':
        return '1-1/2"'
    elif str(first_size) == '1.625':
        return '1-5/8"'
    elif str(first_size) == '1.875':
        return '1-7/8"'
    elif str(first_size) == '2.25':
        return '2-1/4"'
    elif str(first_size) == '2.5':
        return '2-1/2"'
    elif str(first_size) == '2.75':
        return '2-3/4"'
    elif str(first_size) == '3.5':
        return '3-1/2"'
    elif str(first_size) == '0':
        return '-'
    elif str(first_size) == '-':
        return '-'

    first_size = str(first_size).replace('.0', '') + '"'

    return first_size
