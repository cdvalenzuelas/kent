def misscelaneous(description):
    # (VALEC17) VER SI SON FIGURAS EN 8
    if 'FIGURE-8' in description or 'SPECTACLE BLANK' in description:
        return 'F8'

    return '-'
