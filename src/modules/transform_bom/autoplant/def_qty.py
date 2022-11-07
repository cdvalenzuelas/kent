# (VALEC17) DEFINIR LAS CANTIDADES DE LOS ELEMENTOS
def def_qty(row):
    type_code, qty = row

    # (VALEC17) SI ES UNA TUBERÍA ELIMINAR LA CANTIDAD
    if type_code in ['PE', 'BE', 'TE']:
        return '-'

    return qty
