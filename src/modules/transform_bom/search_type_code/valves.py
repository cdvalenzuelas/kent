# (VALEC17) DEFINIR VÁLVULAS
def valves(description):
    # (VALEC17) VER SI SON VALVULAS DE BOLA API 6D
    if 'API 6D' in description and 'BALL' in description:
        return 'BAL6'

    # (VALEC17) VER SI SON VALVULAS DE BOLA NORMALES
    if 'BALL' in description:
        return 'BAL'

    # (VALEC17) VER SI SON VALVULAS DE COMPUERTA API 6D
    if 'API 6D' in description and 'GATE' in description:
        return 'GAT6'

    # (VALEC17) VER SI SON VALVULAS DE BOLA NORMALES
    if 'GATE' in description:
        return 'GAT'

    # (VALEC17) VER SI SON VALVULAS DE GLOBO
    if 'GLOBE' in description or 'ANGLE HOSE VALVE' in description:
        return 'GLB'

    # (VALEC17) VER SI SON VALVULAS DE PLUG
    if 'PLUG' in description:
        return 'PLU'

    # (VALEC17) VER SI SON VALVULAS DBB
    if 'DBB' in description and 'MONO FLANGE' in description:
        return 'DBB'

    # (VALEC17) VER SI SON VALVULAS DE MARIPOSA
    if 'BUTTERFLY' in description:
        return 'BTY'

    # (VALEC17) VER SI SON VALVULAS DE CHEQUE
    if 'CHECK' in description:
        # (VALEC17) VER SI SON CHEQUES SWING Y API 6D
        if 'SWING' in description and 'API 6D' in description:
            return 'CHS6'

        # (VALEC17) VER SI SON CHEQUES SWING
        if 'SWING' in description:
            return 'CHS'

        # (VALEC17) VER SI SON CHEQUES WAFER Y API 6D
        if 'WAFER' in description and 'API 6D' in description:
            return 'CHW6'

        # (VALEC17) VER SI SON CHEQUES WAFER
        if 'WAFER' in description:
            return 'CHW'

        # (VALEC17) VER SI SON CHEQUES LIFT/PISTON/BALL
        if 'LIFT' in description or 'PISTON' in description or 'BALL' in description:
            return 'CHL'

    return '-'
