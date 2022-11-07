# (VALEC17) Definir si la cantidad es la cantidad inicial o la longitud
def pipe_qty(row):
    length, db_code, qty = row

    if db_code in ['PE', 'BE', 'TE']:
        length = float(length)
        return int(length/1000) + 1
    else:
        return int(qty)
