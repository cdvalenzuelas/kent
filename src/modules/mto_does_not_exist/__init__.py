from src.modules.mto_does_not_exist.bom_cleaner import bom_cleaner
from src.modules.mto_does_not_exist.bolts_modifier import bolts_modifier


def mto_does_not_exist():

    # Creación del mto limpio incluyendo la información del piping class
    mto_df = bom_cleaner()

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

    # Agrupar y sumar por cantidad peso y area
    mto_df = mto_df.groupby(['LINE_NUM', 'SPEC', 'ORDER', 'TYPE', 'TYPE_CODE', 'DESCRIPTION', 'FIRST_SIZE',
                             'FIRST_SIZE_NUMBER', 'SECOND_SIZE', 'SECOND_SIZE_NUMBER', 'SCH', 'FACE', 'RATING',
                             'UNITS', 'TAG', 'WEIGHT_PER_UNIT', 'SUPPLY_DESCRIPTION', 'MANUFACTURING_DESCRIPTION',
                             'ERECTION_DESCRIPTION'])[['QTY', 'WEIGHT', 'AREA']].agg(
        TOTAL_WEIGHT=('WEIGHT', sum),
        AREA=('AREA', sum),
        QTY=('QTY', sum))

    # Aqui se pueden reaordenar los lsitados

    # Resetear el index
    mto_df.reset_index(drop=False)

    # Crear el archivo de MTO
    mto_df.to_csv('./output/mto.csv', index=True)
