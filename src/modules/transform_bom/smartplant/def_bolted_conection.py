import pandas as pd

# (VALEC17) CREAR UN INDICE PARA MERGEAR LOS DFS


def common_index(row):
    rating, size, face = row

    return f'{rating} {size} {face}'


def def_bolted_conection(row, piping_class, bom_df):
    line_num, type_code, bolt_diameter, spec, tag = row

    # (VALEC17) SI ES UN ELEMENTO DIFERENTE A PERNOS NO ES NECESARIO BUSCAR EL DIÁMETRO DE LA CONEXIÓN BRIDADA
    if type_code != 'BOLT':
        return bolt_diameter

    # (VALEC17) HACER UNA COPIA DEL PIPING CLASS
    piping_class = piping_class.copy()

    # (VALEC17) lEER EL ARCHIVO DE PERNOS
    bolts = pd.read_csv('./src/clients/cenit/elements/bolts_kent.csv')

    # (VALEC17) FILTRAR EL BOLT-KENT POR EL DIÁMETRO D PERNO
    bolts = bolts[(bolts['BOLT_DIAMETER'] == bolt_diameter)
                  & (bolts['TAG'] == tag)]

    # (VALEC17) FILTRA EL PIPING CLASS POR SPEC Y PERNOS
    piping_class = piping_class[(piping_class['TYPE_CODE'] == 'BOLT') & (
        piping_class['SPEC'] == spec)]

    # (VALEC17) CREAR UN INDICE PARA MERGEAR LOS DFS
    bolts['common_index'] = bolts[['RATING', 'DIAMETER', 'FACE']].apply(
        common_index, axis=1)

    piping_class['common_index'] = piping_class[[
        'RATING', 'FIRST_SIZE', 'FACE']].apply(common_index, axis=1)

    # (VALEC17) HACER UN MERGE
    bolts = pd.merge(bolts, piping_class, how='inner', on='common_index')

    # (VALEC17) DEJAR ÚNICAMENTE LAS COLUMNAS NECESARIAS
    bolts = bolts[['RATING_x', 'DIAMETER', 'FACE_x', 'BOLT_DIAMETER']]

    # (VALEC17) VER SI HAY UN ERROR O SÓLO HAY UNA POSIBILIDAD
    matches = len(bolts)

    if matches == 0:
        return f'{bolt_diameter} WRONG'
    if matches == 1:
        return bolts['DIAMETER'].to_list()[0]

    # (VALEC17) VER SI HAY MÁS DE UNA POSIBILIDAD DE DIÁMETRO

    # (VALEC17) VER CUANTOS RATINGS EXISTEN EN LOS PERNOS ENCONTRADOS
    ratings_qty = len(bolts['RATING_x'].value_counts().to_list())

    # (VALEC17) NORMALIZAR EL NÚMERO DE LÍNEA
    line_num = line_num.replace(' ', '').replace('(U)', '').replace('(P)', '')

    # (VALEC17) FILTRAR EL BOM PARA UE ÚNICAMENTE SE QUEDE EL NÚMERO DE LÍNEA DEL PERNO Y LA BRIDAS EXISTENTES Y LOS GASKETS
    bom_df = bom_df[(bom_df['LINE_NUM'] == line_num) & (
        bom_df['DB_CODE'].isin(['SW', 'WNK', 'BLD', 'ORF', 'GAS', 'KIT']))]

    # (VALEC17) VER LOS DIÁMETROS UE CUENTAN CON BRIDAS Y GASKETS EN LÍNEA
    uniques_diameters = set(bom_df['MAIN_NOM'].values)

    # (VALEC17) SI SÓLO HAY UN RATING DEJAR LOS DIÁMETROS POSIBLES
    if ratings_qty == 1:
        # (VALEC17) VER LOS DIÁMETROS DE LAS UNIONES PERNADAS DETECTADAS
        bolted_conections_detected = set(bolts['DIAMETER'].to_list())

        # (VALEC17) HCER LA INTERSECCIÓN ENTRE  LOS DIÁMETROS DE LA LÍNEA Y LOS DIAMETROS DE LAS UNIONES PERNADAS DETECTADAS
        intersections = uniques_diameters.intersection(
            bolted_conections_detected)

        # (VALEC17) PASAR EL SET A LIST
        intersections = list(intersections)

        # (VALEC17) SI YA SE ENCONTRÓ EL DIÁMETRO RETORNARLO
        if len(intersections) == 1:
            return intersections[0]

        return str(intersections)

    # print(len(bolts))
    print('--------------------------')

    return f'{bolt_diameter} WRONG'
