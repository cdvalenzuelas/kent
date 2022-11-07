# (VALEC17) DEFINIR LOS STRAINERS
def strainers(description):
    # (VALEC17) VER SI SON FILTROS DE TIPO CANASTA
    if 'BASKET' in description:
        return 'BST'

    # (VALEC17) VER SI SON FILTROS DE TIPO Y
    if 'Y-TYPE' in description or '"Y" TYPE' in description:
        return 'YST'

    # (VALEC17) VER SI SON FILTROS DE TIPO T
    if 'T-TYPE' in description:
        return 'TST'

    # (VALEC17) VER SI SON FILTROS DE TIPO TEMPORARY START-UP
    if 'TEMPORARY START-UP' in description:
        return 'SST'

    return '-'
