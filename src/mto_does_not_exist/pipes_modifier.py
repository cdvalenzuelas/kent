# Definir si la cantidad es la cantidad inicial o la longitud
def pipe_qty(row):
    length, db_code, qty = row

    if db_code in ['PE', 'BE', 'TE']:
        return int(length/1000) + 1
    else:
        return qty
