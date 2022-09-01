import pandas as pd


# (VALEC17) Se le coloca un área distinta a cero a las válvulas, gaskets, bolts y miscelaneos
def areas(row):
    area, type_element = row

    if type_element in ['VL', 'GS', 'BL', 'MS']:
        return 1
    else:
        return area


# (VALEC17) Camuflar a los elementos que no necesitan prefabricación
def def_manufacturing_description(row):
    type_code, manufacturing_description = row

    if type_code in ['BOLT', 'GAS', 'F8', 'YST']:
        return 'a'
    else:
        return manufacturing_description


# (VALEC17) Crear un archivo temporal que indique que items tienen información faltante em las cantidades de obra
def co_temp(co_df):
    # (VALEC17) Hacer una copia del co_df
    co_df = co_df.copy()

    # (VALEC17) Se le coloca un área distinta a cero a las válvulas, gaskets, bolts y miscelaneos
    co_df['AREA'] = co_df[['AREA', 'TYPE']].apply(areas, axis=1)

    # (VALEC17) Camuflar a los elementos que no necesitan prefabricación
    co_df['MANUFACTURING_DESCRIPTION'] = co_df[['TYPE_CODE', 'DESCRIPTION']].apply(
        def_manufacturing_description, axis=1)

    # (VALEC17) Mostrar únicamente a los items que no tienen información de cantidades de obra
    co_df = co_df[(co_df['SUPPLY_DESCRIPTION'] == '-') | (co_df['AREA'] == 0) | (co_df['WEIGHT_PER_UNIT'] == 0) |
                  (co_df['MANUFACTURING_DESCRIPTION'] == '-') | (co_df['ERECTION_DESCRIPTION'] == '-')]

    # (VALEC17) Eliminar columnas innecesarias
    co_df.drop(['TYPE', 'FIRST_SIZE_NUMBER',
                'SECOND_SIZE_NUMBER', 'UNITS', 'TOTAL_WEIGHT', 'QTY', 'UNITS'], inplace=True, axis=1)

    if co_df.shape[0] == 0:
        print('✅ TODOS LOS ELEMENTOS DEL B.O.M TIENEN RELACIONADOS CANTIDADES DE OBRA\n')
    else:
        print(
            '❌  EXISTEN ELEMENTOS DEL B.O.M QUE NO TIENEN RELACIONADAS CANTIDADES DE OBRA\n')
        # (VALEC17) Guardar el archivo
        co_df.to_csv('./output/co_temp.csv', index=False)
