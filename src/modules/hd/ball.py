# Crear índices
from operator import index


def create_index(row):
    spec, tag, type_code, rating, service, design_pressure, design_temperature, valve_type, connection, end_code, bore, operator, body, bonnet_gasket, ball, stem, other, seals, seat, packing, api_trim, length, design_code, test_pressure, aplicable_standards, bore_according_to, coating, system = row

    return f'{spec} {tag} {type_code} {rating} {service} {design_pressure} {design_temperature} {valve_type} {connection} {end_code} {bore} {operator} {body} {bonnet_gasket} {ball} {stem} {other} {seals} {seat} {packing} {api_trim} {length} {design_code} {test_pressure} {aplicable_standards} {bore_according_to} {coating} {system}'


def ball(valves_df):
    # Extrayendo únicamente las válvulas de bola
    valves_df = valves_df[valves_df['TYPE_CODE'].str.startswith('BAL')]

    # Ordenar las válvulas
    valves_df.sort_values(by=['SPEC', 'TAG', 'TYPE_CODE', 'RATING', 'SERVICE',
                              'DESIGN_PRESSURE', 'DESIGN_TEMPERATURE', 'TYPE', 'CONECTION',
                              'END_CODE', 'BORE', 'OPERATOR', 'BODY', 'BONNET_GASKET', 'BALL',
                              'STEAM', 'OTHER', 'SEALS', 'SEAT', 'PACKING', 'API_TRIM', 'LENGTH',
                                                 'DESIGN_CODE', 'TEST_PRESSURE', 'APPLICABLE_STANDARDS',
                                                 'BORE_ACCORDING_TO', 'COATING', 'SYSTEM', 'SIZE_NUMBER', 'SIZE'], inplace=True)

    # Eliminar duplicados
    valves_df.drop_duplicates(['SPEC', 'TAG', 'TYPE_CODE', 'SIZE_NUMBER', 'SIZE', 'RATING', 'SERVICE',
                               'DESIGN_PRESSURE', 'DESIGN_TEMPERATURE', 'TYPE', 'CONECTION',
                               'END_CODE', 'BORE', 'OPERATOR', 'BODY', 'BONNET_GASKET', 'BALL',
                               'STEAM', 'OTHER', 'SEALS', 'SEAT', 'PACKING', 'API_TRIM', 'LENGTH',
                                                 'DESIGN_CODE', 'TEST_PRESSURE', 'APPLICABLE_STANDARDS',
                                                 'BORE_ACCORDING_TO', 'COATING', 'SYSTEM'], keep='first', inplace=True)

    # Crear índices
    valves_df['index_2'] = valves_df[['SPEC', 'TAG', 'TYPE_CODE', 'RATING', 'SERVICE',
                                      'DESIGN_PRESSURE', 'DESIGN_TEMPERATURE', 'TYPE', 'CONECTION',
                                      'END_CODE', 'BORE', 'OPERATOR', 'BODY', 'BONNET_GASKET', 'BALL',
                                      'STEAM', 'OTHER', 'SEALS', 'SEAT', 'PACKING', 'API_TRIM', 'LENGTH',
                                      'DESIGN_CODE', 'TEST_PRESSURE', 'APPLICABLE_STANDARDS',
                                      'BORE_ACCORDING_TO', 'COATING', 'SYSTEM']].apply(create_index, axis=1)

    # Sacar aparte todos los indices distintos
    indexes = valves_df[['index_2']]

    indexes.drop_duplicates(['index_2'], inplace=True, keep='first')

    print(indexes)
