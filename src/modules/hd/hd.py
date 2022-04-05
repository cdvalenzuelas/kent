import pandas as pd


from src.modules.hd.ball import ball


def valves_index(row):
    spec, size, tag = row

    return f'{spec} {size} {tag}'


def hd():
    # leer el archivo de válvulas
    valves_df = pd.read_csv(
        './src/clients/cenit/elements/cenit_valves_tags.csv')

    # leer el MTO creado
    mto_df = pd.read_csv('./src/output/mto.csv')

    # Extrayendo únicamente las válvulas
    mto_df = mto_df[mto_df['TYPE'] == 'VL']

    # Extrayendo Las columnas necesarias del MTO
    mto_df = mto_df[['SPEC', 'FIRST_SIZE_NUMBER', 'TAG']]

    # Crear un índice común entre el mto y la tabla de válvulas
    valves_df['valves_index'] = valves_df[['SPEC', 'SIZE_NUMBER', 'TAG']].apply(
        valves_index, axis=1)

    mto_df['valves_index'] = mto_df[['SPEC', 'FIRST_SIZE_NUMBER', 'TAG']].apply(
        valves_index, axis=1)

    # Crear el merge entre las dos tablas
    valves_df = pd.merge(mto_df, valves_df, how='left', on='valves_index')

    valves_df.drop(['SPEC_y', 'TAG_y', 'valves_index',
                   'FIRST_SIZE_NUMBER'], inplace=True, axis=1)

    valves_df.rename({'SPEC_x': 'SPEC', 'TAG_x': 'TAG'}, inplace=True, axis=1)

    ball(valves_df)

    return 1
