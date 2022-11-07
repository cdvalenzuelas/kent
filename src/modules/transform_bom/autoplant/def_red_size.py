def def_red_size(row):
    type_code, size = row

    if type_code in ['RTE', 'WOL', 'TOL', 'SOL', 'CRE', 'ERE', 'SWC']:
        red_size = size.upper().replace(' ', '').split('X')[
            1].replace('+', '-') + '"'

        return red_size

    return '-'
