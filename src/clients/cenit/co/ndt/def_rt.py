# (VALEC17) Calcular pruebas radiográficas
def def_rt(row, ndt_dict):
    spec, bw, sw, tw = row

    total = bw*ndt_dict[spec]['BW']['RT'] + sw * \
        ndt_dict[spec]['SW']['RT'] + tw*ndt_dict[spec]['TW']['RT']

    return total
