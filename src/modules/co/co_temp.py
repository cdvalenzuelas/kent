import pandas as pd


def areas(row):
    area, type_element = row

    if type_element in ['VL', 'GS', 'BL', 'MS']:
        return 1
    else:
        return area


# Crear un archivo temporal que indique que items tienen información faltante em las cantidades de obra
def co_temp():
    co_df = pd.read_csv('./output/mto.csv')

    co_df['AREA'] = co_df[['AREA', 'TYPE']].apply(areas, axis=1)

    co_df = co_df[(co_df['SUPPLY_CODE'] == '-') | (co_df['SUPPLY_TITLE'] == '-') | (
        co_df['SUPPLY_DESCRIPTION'] == '-') | (co_df['AREA'] == 0) | (co_df['WEIGHT_PER_UNIT'] == 0)]

    co_df.drop(['ORDER', 'TYPE', 'FIRST_SIZE_NUMBER',
                'SECOND_SIZE_NUMBER', 'UNITS', 'TOTAL_WEIGHT', 'QTY', 'SCH', 'FACE', 'RATING', 'UNITS', 'TAG'], inplace=True, axis=1)

    co_df.to_csv('./output/co_temp.csv')
