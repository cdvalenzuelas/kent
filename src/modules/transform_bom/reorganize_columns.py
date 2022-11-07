import pandas as pd
import numpy as np

# (VALEC17) RENOMBRAR LAS COLUMNAS


def rename_columns(new_column, bom_df):
    set_new_columns = set(new_column)
    bom_df_columns = bom_df.columns.to_list()

    cad_software = ''

    # (DETECTAR DE DONDE VIENE LA EXTRACCIÓN)
    autoplant_columns = {'ITEM', 'LINE NUMBER', 'GTYPE', 'STYPE', 'SPEC', 'SCHEDULE',
                         'RATING', 'FACING', 'COMPONENT DESCRIPTION', 'UNITS', 'QUANTITY', 'PESO'}
    cadworks_columns = {'MARK',	'LINE_NUM',	'SPEC_FILE', 'DB_CODE', 'DESCRIPTION',
                        'SHORT_DESC',	'SIZE',	'MAIN_NOM',	'RED_NOM',	'THK_NOM',	'QTY',	'TAG',	'LENGTH',	'WEIGHT'}
    smartplant_columns = {'ITEM', 'AREA', 'NUMERO DE LÍNEA', 'SPEC', 'TYPE (VER HOJA ABREVIATURAS)', 'TYPE CODE (VER HOJA ABREVIATURAS)', 'DESCRIPCIÓN', 'DIAMETRO PRINCIPAL',
                          'DIAMETRO DE BIFURCACIÓN / DIÁMETRO REDUCCIÓN / LONGITUD DE PERNOS / LONGITUD DE NIPLES', 'SCHEDULE', 'FACE', 'RATING', 'CANTIDAD TOTAL', 'UNIDAD', 'PESO UNITARIO', 'PESO TOTAL'}

    if len(set_new_columns.intersection(autoplant_columns)) == len(autoplant_columns):
        cad_software = 'autoplant'

        new_column[10] = 'SIZE'
        new_column[15] = np.nan
        new_column[16] = 'RATING'
        new_column[28] = 'PESO TOTAL'
    elif len(set_new_columns.intersection(cadworks_columns)) == len(cadworks_columns):
        cad_software = 'cadworks'
    elif len(set_new_columns.intersection(smartplant_columns)) == len(smartplant_columns):
        cad_software = 'smartplant'

    # (VALEC17) ARMAR EL DICCIONARIO DE RENOMBRES
    rename_dict = {}

    for index, old_name in enumerate(bom_df_columns):
        rename_dict[old_name] = new_column[index]

    bom_df.rename(columns=rename_dict, inplace=True)

    bom_df.reset_index(inplace=True, drop=True)

    return bom_df, cad_software

# (VALEC17) REORGANIZAR LAS COLUMNAS


def reorganize_columns():
    # (VALEC17) LEER EL BOM
    bom_df = pd.read_csv('./inputs/bom.csv')

    # (VALEC17) ITERAR EL BOM HASTA ENCONTRAR DESDE DONDE EMPIEZAN LAS COLUMNAS
    new_index = 0
    new_columns = []

    for index, row in bom_df.iterrows():
        row_list = row.to_list()

        if str(row_list[0]) == 'nan':
            new_index += 1
        else:
            # (VALEC17) SI SE ENCUENTRAN LAS COLUMNAS DE UNA DEJARLAS
            if new_index == 0:
                new_columns = bom_df.columns.to_list()
            else:
                new_columns = row_list
            break

    # (VALEC17) RECRTAR EL DATAFRAME HASTA ENCONTRAR LAS COLUMNAS
    bom_df = bom_df.iloc[new_index:]

    bom_df, cad_software = rename_columns(new_columns, bom_df)

    # (VALEC17) RETORNAR EL DF ARREGLADO Y Y NOMBRE DEL PROGRAMA DE DISEÑO
    return(bom_df, cad_software)
