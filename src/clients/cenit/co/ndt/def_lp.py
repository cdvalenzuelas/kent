# Calcular tintas penetrantes
def def_lp(row, ndt_dict):
    spec, bw, sw, tw = row

    total = bw*ndt_dict[spec]['BW']['LP'] + sw * \
        ndt_dict[spec]['SW']['LP'] + tw*ndt_dict[spec]['TW']['LP']

    return total
