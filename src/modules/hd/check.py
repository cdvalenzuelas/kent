from src.modules.hd.general_fields import general_fields

def check(row, wb, valve_type):  
    # Llenando los campos generales 
    wb, sheet_name = general_fields(row, wb, valve_type)

    # Seleccionando la hoja correcta
    sheet = wb[sheet_name]

    # MATERIALS, SÓLO PARA VÁLVULAS DE BOLA
    sheet['H31'] = row['BODY']
    sheet['AC31'] = row['API_TRIM'] if row['API_TRIM'] != '-' else 'BY MNF'
    sheet['H32'] = row['BONNET_GASKET']
    sheet['AC32'] = row['PACKING'] if row['PACKING'] != '-' else 'BY MNF'
    sheet['H33'] = row['SEAT'] if row['SEAT'] != '-' else 'BY MNF'
    sheet['AC33'] = row['SEALS'] if row['SEALS'] != '-' else 'BY MNF'    
    sheet['H34'] = row['SYSTEM'] if row['SYSTEM'] != '-' else ''
    sheet['H35'] = row['COATING'] if row['COATING'] != '-' else 'BY MNF'
    sheet['H37'] = row['OTHER'] if row['OTHER'] != '-' else '' 

    # returnr el wb
    return wb