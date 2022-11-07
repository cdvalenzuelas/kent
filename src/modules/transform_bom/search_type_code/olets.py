def olets(description):
    # (VALEC17) VER SI ES UN SOCKOLET
    if 'SOCKOLET' in description:
        return 'SOL'

    # (VALEC17) VER SI ES UN WELDOLET
    if 'WELDOLET' in description:
        return 'WOL'

    # (VALEC17) VER SI ES THREADOLET
    if 'THREADOLET' in description:
        return 'TOL'

    return '-'
