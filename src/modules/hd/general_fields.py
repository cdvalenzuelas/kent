def general_fields(row, wb, valve_type):
    # (VALEC17) Determinar los nombres de las hojas
    tags = wb.sheetnames

    sheet_name = ''

    if row['TAG'] not in tags:
        sheet_name = row['TAG']
    else:
        tag_coincidences = len(
            [1 for tag in tags if tag.startswith(row['TAG'])])
        sheet_name = f'{row["TAG"]} ({tag_coincidences})'

    # (VALEC17) Copiar la hoja desde el template
    old_sheet = wb[valve_type]
    sheet = wb.copy_worksheet(old_sheet)

    # (VALEC17) renombrando la hoja nueva
    sheet.title = sheet_name

    # (VALEC17) LLENANDO CONDICIONES GENERALES COMÚN A TODAS LAS VÁLVULAS
    sheet['H3'] = row['TAG']
    sheet['H4'] = row['SIZES']
    sheet['H5'] = row['SPEC']
    sheet['H6'] = row['SERVICE']

    # (VALEC17) LLENANDO LA PARTE MECÁNICA QUE S COMÚN A TODAS LAS VÁLVULAS
    sheet['H10'] = row['TYPE']
    sheet['AC10'] = row['RATING']
    sheet['L11'] = 'X' if row['CONECTION'] in ['RF', 'FF', 'RTJ'] else ''
    sheet['T11'] = row['CONECTION'] if sheet['L11'].value == 'X' else ''
    sheet['AC11'] = 'X' if row['CONECTION'] == 'SW' else ''
    sheet['AH11'] = 'X' if row['CONECTION'] == 'SCREWED' else ''
    sheet['L12'] = 'X' if row['CONECTION'] == 'BUTWELD' else ''
    sheet['AD12'] = row['CONECTION'] if row['CONECTION'] not in [
        'RF', 'FF', 'RTJ', 'SW', 'SCREWED', 'BUTWELD'] else ''
    sheet['Q14'] = 'X' if row['END_CODE'] == 'ASME B16.5' else ''
    sheet['Y14'] = 'X' if row['END_CODE'] == 'ASME B16.11' else ''
    sheet['AF14'] = row['END_CODE'] if row['END_CODE'] not in [
        'ASME B16.5', 'ASME B16.11'] else ''
    sheet['H17'] = row['OPERATOR'] if row['OPERATOR'] != '-' else ''

    # (VALEC17) DESIGN COMUNES A TODAS LAS VÁLVULAS
    sheet['I22'] = 'X' if row['DESIGN_CODE'] == 'API 600' else ''
    sheet['O22'] = 'X' if row['DESIGN_CODE'] == 'API 6D' else ''
    sheet['U22'] = 'X' if row['DESIGN_CODE'] == 'API 608' else ''
    sheet['AA22'] = 'X' if row['DESIGN_CODE'] == 'API 602' else ''
    sheet['AG22'] = row['DESIGN_CODE'] if row['DESIGN_CODE'] not in [
        'API 600', 'API 6D', 'API 602', 'API 608'] else ''
    sheet['L23'] = row['APPLICABLE_STANDARDS'] if row['APPLICABLE_STANDARDS'] != '-' else ''
    sheet['H24'] = row['DESIGN_PRESSURE']
    sheet['AB24'] = row['DESIGN_TEMPERATURE']
    sheet['AF24'] = 100
    sheet['AB25'] = row['TEST_PRESSURE'] if row['TEST_PRESSURE'] != '-' else ''

    # (VALEC17) Retornar el WB
    return (wb, sheet_name)
