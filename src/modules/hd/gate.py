from src.modules.hd.general_fields import general_fields


def gate(row, wb, valve_type):
    # (VALEC17) Llenando los campos generales
    wb, sheet_name = general_fields(row, wb, valve_type)

    # (VALEC17) Seleccionando la hoja correcta
    sheet = wb[sheet_name]

    # (VALEC17) MATERIALS, SÓLO PARA VÁLVULAS DE BOLA
    sheet['H31'] = row['BODY']
    sheet['H32'] = row['BONNET_GASKET']
    sheet['AC31'] = row['PACKING'] if row['PACKING'] != '-' else 'BY MNF'
    sheet['H33'] = row['SEALS'] if row['SEALS'] != '-' else 'BY MNF'
    sheet['H34'] = row['STEM'] if row['STEM'] != '-' else 'BY MNF'
    sheet['H35'] = row['SEAT'] if row['SEAT'] != '-' else 'BY MNF'
    sheet['H36'] = row['COATING'] if row['COATING'] != '-' else 'BY MNF'
    sheet['H38'] = row['OTHER'] if row['OTHER'] != '-' else ''

    # (VALEC17) returnr el wb
    return wb
