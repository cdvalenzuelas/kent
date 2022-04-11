import pandas as pd


# Se le coloca un área distinta a cero a las válvulas, gaskets, bolts y miscelaneos
def areas(row):
    area, type_element = row

    if type_element in ['VL', 'GS', 'BL', 'MS']:
        return 1
    else:
        return area


# Camuflar a los elementos que no necesitan prefabricación
def def_manufacturing_description(row):
    type_code, manufacturing_description = row

    if type_code in ['BOLT', 'GAS', 'F8', 'YST']:
        return 'a'
    else:
        return manufacturing_description


# Crear un archivo temporal que indique que items tienen información faltante em las cantidades de obra
def co_temp():
    # Se lee el mto
    co_df = pd.read_csv('./output/mto.csv')

    # Se le coloca un área distinta a cero a las válvulas, gaskets, bolts y miscelaneos
    co_df['AREA'] = co_df[['AREA', 'TYPE']].apply(areas, axis=1)

    # Camuflar a los elementos que no necesitan prefabricación
    co_df['MANUFACTURING_DESCRIPTION'] = co_df[['TYPE_CODE', 'DESCRIPTION']].apply(
        def_manufacturing_description, axis=1)

    # Mostrar únicamente a los items que no tienen información de cantidades de obra
    co_df = co_df[(co_df['SUPPLY_DESCRIPTION'] == '-') | (co_df['AREA'] == 0) | (co_df['WEIGHT_PER_UNIT'] == 0) |
                  (co_df['MANUFACTURING_DESCRIPTION'] == '-') | (co_df['ERECTION_DESCRIPTION'] == '-')]

    # Eliminar columnas innecesarias
    co_df.drop(['LINE_NUM', 'ORDER', 'TYPE', 'FIRST_SIZE_NUMBER',
                'SECOND_SIZE_NUMBER', 'UNITS', 'TOTAL_WEIGHT', 'QTY', 'SCH', 'FACE', 'RATING', 'UNITS', 'TAG'], inplace=True, axis=1)

    # Guardar el archivo
    co_df.to_csv('./output/co_temp.csv', index=False)
