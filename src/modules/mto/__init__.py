from src.modules.bom_clenaer.bom_cleaner import bom_cleaner
from src.modules.bolts_modifier.bolts_modifier import bolts_modifier
import numpy as np


# Calcular el área total de cada elemento
def def_total_area(row):
    type_element, area, qty = row

    if type_element == '-':
        return 0

    area = float(area)
    qty = float(qty)

    if type_element == 'PP':
        return 1.1 * np.pi * qty * (area / 1000)
    else:
        return 1.1 * area * qty


def mto(bom_df, piping_class, piping_class_valves_weights):

    # Creación del mto limpio incluyendo la información del piping class
    mto_df = bom_cleaner(bom_df, piping_class, piping_class_valves_weights)

    # Crear registro de items sin identificar
    mto_df_na = mto_df[(mto_df['DESCRIPTION'].isnull())
                       | (mto_df['DESCRIPTION'] == '-')]

    # Si se encontraron todos lo elementos en el piping class decirlo, de lo contrario alertarlo
    if mto_df_na.shape[0] == 0:
        print('\n✅ SE ENCONTRARON TODOS LOS ELEMENTOS DEL B.O.M EN EL PIPING CLASS\n')
    else:
        print('\n❌ HAY ELEMENTOS EN EL B.O.M QUE NO SE ENCUENTRAN EN EL PIPING CLASS\n')

        mto_df_na = mto_df_na[['LINE_NUM', 'QTY', 'common_index']]

        mto_df_na.to_csv('./output/mto_temp.csv', index=True)

    # Limpiar el mto

    mto_df = mto_df[mto_df['DESCRIPTION'] != '-']

    # Modificación por pernos
    mto_df = bolts_modifier(mto_df=mto_df)

    # Creando la columna weight per unit
    mto_df['WEIGHT_PER_UNIT'] = mto_df['WEIGHT']

    # Multiplicando pesos
    mto_df['WEIGHT'] = mto_df['WEIGHT_PER_UNIT']*mto_df['QTY']

    # Convertir datos
    mto_df.convert_dtypes().dtypes

    # Eliminar columnas innecesarias
    mto_df.drop(['common_index'], axis=1, inplace=True)

    # Mto que será utilizado para CO
    mto_df_for_co = mto_df.copy()

    # Agrupar y sumar por cantidad peso y area
    mto_df = mto_df.groupby(['LINE_NUM', 'SPEC', 'ORDER', 'TYPE', 'TYPE_CODE', 'DESCRIPTION', 'FIRST_SIZE',
                             'FIRST_SIZE_NUMBER', 'SECOND_SIZE', 'SECOND_SIZE_NUMBER', 'SCH', 'FACE', 'RATING',
                             'UNITS', 'TAG', 'WEIGHT_PER_UNIT'], as_index=False)[['QTY', 'WEIGHT', 'AREA']].agg(
        TOTAL_WEIGHT=('WEIGHT', sum),
        AREA=('AREA', sum),
        QTY=('QTY', sum))

    # Se calcula el área total por elemento
    mto_df_for_co['AREA'] = mto_df_for_co[[
        'TYPE', 'AREA', 'QTY']].apply(def_total_area, axis=1)

    mto_df_for_co.to_excel('co.xlsx')

    # Hacer el sumario para las cantidades de obra
    mto_df_for_co = mto_df_for_co.groupby(['SPEC', 'TYPE', 'TYPE_CODE', 'DESCRIPTION',
                                           'FIRST_SIZE_NUMBER', 'SECOND_SIZE_NUMBER', 'FACE',
                                           'UNITS', 'WEIGHT_PER_UNIT', 'SUPPLY_DESCRIPTION', 'MANUFACTURING_DESCRIPTION',
                                           'ERECTION_DESCRIPTION', 'UNDERGROUND', 'PRE_MANUFACTURING'], as_index=False)[['QTY', 'WEIGHT', 'AREA']].agg(
        TOTAL_WEIGHT=('WEIGHT', sum),
        AREA=('AREA', sum),
        QTY=('QTY', sum))

    # Resetear el index
    mto_df.reset_index(drop=False)

    return (mto_df, mto_df_for_co)
