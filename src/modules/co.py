import pandas as pd


def unidad(item_type):
    if item_type == 'PP':
        return 'M'
    else:
        return 'U.N'


def supply():
    # Leer el MTO
    co_df = pd.read_csv('./src/output/mto.csv')

    co_df['UNIDAD'] = co_df['TYPE'].apply(unidad)

    # Seleccionar únicamente las columnas necesarias
    co_df = co_df[['CO', 'SUPPLY', 'UNIDAD', 'QTY']]

    co_df = co_df[co_df['CO'] != '-']

    # Agrupar y sumar por cantidad peso y area
    co_df = co_df.groupby(['CO', 'SUPPLY', 'UNIDAD']).agg(QTY=('QTY', sum))

    # Resetear el index
    co_df = co_df.reset_index(drop=False)

    co_df.rename(columns={'CO': 'CAPÍTULO',
                 'SUPPLY': 'DESCRIPCIÓN', 'QTY': 'CANTIDAD'}, inplace=True)

    return co_df


def description_pre_manufacturing(row):
    co, descrption, size = row


def pre_manufacturing():
    # Leer el MTO
    co_df = pd.read_csv('./src/output/mto.csv')

    # Unidades de prefabricación
    co_df['UNIDAD'] = 'KG'

    co_df['CAPÍTULO'] = co_df['CO_2.1']

    co_df['DESCRIPCIÓN'] = co_df[['CAPÍTULO', 'CO_2.2', 'FIRST_SIZE']].apply(
        description_pre_manufacturing, axis=1)


def co():
    # Suministros
    supply_df = supply()
    pre_manufacturing_df = pre_manufacturing()

    # Crear el archivo summary
    #co_df.to_csv('./src/output/co.csv', index=True)
