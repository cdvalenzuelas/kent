def detect_cad_software(bom_df):
    # Hacer una copia del df
    bom_df = bom_df.copy()

    # Columnas de la extracción
    bom_columns = bom_df.columns.tolist()

    cad_software = ''

    # Definir columnas de los software
    autoplant_columns = {'ITEM', 'LINE NUMBER', 'GTYPE', 'STYPE', 'SPEC', 'SIZE',
                         'SCHEDULE', 'RATING', 'FACING', 'COMPONENT DESCRIPTION', 'UNITS', 'QUANTITY', 'PESO'}

    cadworks_columns = {'MARK', 'LINE_NUM', 'SPEC_FILE', 'DB_CODE', 'DESCRIPTION',
                        'SHORT_DESC', 'SIZE', 'MAIN_NOM', 'RED_NOM', 'THK_NOM', 'QTY', 'TAG', 'LENGTH', 'WEIGHT'}

    # Determinar de que software viene la extracción
    if len(autoplant_columns - set(bom_columns)) == 0:
        bom_df.to_csv('./inputs/bom_autoplant.csv', index=False)
        return 'autoplant'
    elif len(cadworks_columns - set(bom_columns)) == 0:
        return 'cadworks'
    else:
        return None
