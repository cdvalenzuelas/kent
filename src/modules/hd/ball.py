from src.modules.hd.general_fields import general_fields

def ball(row, wb, valve_type):  
    # Llenando los campos generales 
    wb, sheet_name = general_fields(row, wb, valve_type)

    # Seleccionando la hoja correcta
    sheet = wb[sheet_name]     

    # CONDICIONES MECÁNICAS PARA LAS VÁLVULAS DE BOLA
    sheet['J15'] = 'X' if row['BORE'] == 'FULL' else ''
    sheet['T15'] = 'X' if row['BORE'] == 'REDUCED' else ''
    sheet['AE15'] = row['BORE_ACCORDING_TO'] if row['BORE_ACCORDING_TO'] != '-' else ''
    sheet['P16'] = 'X' if row['LENGTH'] == 'SHORT' else '' #SÓLO PARA VÁLVULAS DE BOLA
    sheet['AA16'] = 'X' if row['LENGTH'] == 'LONG' else '' #SÓLO PARA VÁLVULAS DE BOLA    

    # MATERIALS, SÓLO PARA VÁLVULAS DE BOLA
    sheet['H31'] = row['BODY']
    sheet['H32'] = row['BONNET_GASKET']
    sheet['AC31'] = row['PACKING'] if row['PACKING'] != '-' else 'BY MNF'
    sheet['H33'] = row['SEALS'] if row['SEALS'] != '-' else 'BY MNF'
    sheet['H34'] = row['BALL'] if row['BALL'] != '-' else 'BY MNF'
    sheet['H35'] = row['STEM'] if row['STEM'] != '-' else 'BY MNF'
    sheet['H36'] = row['SEAT'] if row['SEAT'] != '-' else 'BY MNF'
    sheet['H37'] = row['COATING'] if row['COATING'] != '-' else 'BY MNF'
    sheet['H39'] = row['OTHER'] if row['OTHER'] != '-' else ''

    # returnr el wb
    return wb
    

    

    
