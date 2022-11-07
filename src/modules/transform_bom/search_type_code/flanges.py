def flanges(description):
    # (VALEC17) VER SI SON DE ORIFICIO
    if 'ORIFICE' in description:
        return 'ORF'

    # (VALEC17) VER SI SON CIEGAS
    if 'BLIND' in description:
        return 'BLD'

    # (VALEC17) VER SI SON WELDING NECK
    if 'NECK' in description:
        return 'WNK'

    # (VALEC17) VER SI SON CIEGAS
    if 'SOCKETWELD' in description:
        return 'SW'

    return '-'
