from src.utils.normalize_string import normalize_string


# Encontral la celda y colocar el valor
def def_qty(row, rt_cell, rt_total, lp_cell, lp_total):
    description, qty = row

    if normalize_string(description) == rt_cell:
        return round(rt_total*1.2, 2)
    elif normalize_string(description) == lp_cell:
        return round(lp_total*1.2, 2)
    else:
        return qty
