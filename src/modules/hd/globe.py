from src.modules.hd.general_fields import general_fields

def globe(row, wb, valve_type):  
    # Llenando los campos generales 
    wb, sheet_name = general_fields(row, wb, valve_type)

    # Seleccionando la hoja correcta
    sheet = wb[sheet_name]

    # MATERIALS, SÓLO PARA VÁLVULAS DE BOLA
    sheet['H31'] = row['BODY']
    sheet['AC31'] = row['API_TRIM'] if row['API_TRIM'] != '-' else ''    
    sheet['H32'] = row['BONNET_GASKET']
    sheet['AC32'] = row['PACKING'] if row['PACKING'] != '-' else 'BY MNF'
    sheet['H33'] = 'BY MNF'
    sheet['AC33'] = row['SEALS'] if row['SEALS'] != '-' else 'BY MNF'
    sheet['H34'] = row['STEM'] if row['STEM'] != '-' else 'BY MNF'
    sheet['H35'] = row['SEAT'] if row['SEAT'] != '-' else 'BY MNF'
    sheet['H36'] = row['COATING'] if row['COATING'] != '-' else 'BY MNF'
    sheet['H38'] = row['OTHER'] if row['OTHER'] != '-' else ''

    # returnr el wb
    return wb