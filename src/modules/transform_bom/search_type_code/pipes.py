def pipes(description):
    # (VALEC17) VER SI ES BE
    if ', BE,' in description or ', BE' in description:
        return 'BE'

    # (VALEC17) VER SI ES PE
    if ', PE,' in description or ', PE' in description:
        return 'PE'

    # (VALEC17) VER SI ES TE
    if ', TE,' in description or ', TE' in description:
        return 'TE'

    return '-'
