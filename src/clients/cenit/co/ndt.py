import pandas as pd

from src.utils.normalize_string import normalize_string


# Calcular las soldaduras por cada elementos
def welds_per_element(row):
    type_element, type_code, first_size_number, second_size_number, qty, face = row

    first_size_number = float(first_size_number)
    second_size_number = float(second_size_number)

    if type_code in ['WNK', 'SW', 'CAP', 'LAP', 'ORF']:
        return first_size_number*qty

    if type_code in ['SOL', 'WOL', 'LOL']:
        return second_size_number * qty

    if type_code in ['90L', '45L', 'CPL', 'UNN', 'SLP']:
        return 2*first_size_number*qty

    if type_code in ['TEE']:
        return 3*first_size_number*qty

    if type_code in ['CRE', 'ERE']:
        return (first_size_number + second_size_number)*qty

    if type_code in ['RTE']:
        return (2*first_size_number + second_size_number)*qty

    if type_code in ['SWC', 'SWE']:
        # OJO DEPENDE DEL FACE
        return (first_size_number + second_size_number)*qty

    if type_code in ['PE', 'BE']:
        int_division = int(qty/6)

        if qty/6 > int_division:
            return int_division
        else:
            if int_division == 0:
                return 0
            else:
                return int_division - 1

    if type_code in ['NIP', 'TE', 'TOL', 'BLD', 'THD']:
        return 0


# Coloca el segundo diámetro corecto (elimina basura)
def def_second_size_number(row):
    type_element, type_code, second_size_number = row

    if second_size_number == '-':
        return 0

    if type_code == 'NIP':
        return 0

    return second_size_number


# Definir la cantidad de soldaduras BW
def def_bw(row):
    face, type_code, diametric_welds, first_size_number, second_size_number, qty = row

    first_size_number = float(first_size_number)
    second_size_number = float(second_size_number)

    if face in ['BE', 'BW']:
        return diametric_welds

    if type_code in ['WNK', 'ORF']:
        return diametric_welds

    if type_code in ['SWC', 'SWE']:
        if face in ['BExPE', 'BWxPE', 'BExTE', 'BWxTE', 'BExTHD', 'BWxTHD']:
            return first_size_number * qty

    return 0


# Definir la cantidad de soldaduras SW
def def_sw(row):
    face, type_code, diametric_welds, first_size_number, second_size_number, qty = row

    first_size_number = float(first_size_number)
    second_size_number = float(second_size_number)

    if face in ['PE', 'SW']:
        return diametric_welds

    if type_code in ['SW']:
        return diametric_welds

    if type_code in ['SWC', 'SWE']:
        if face in ['BExPE', 'BWxPE', 'TExPE', 'THDxPE', 'BExSW', 'BWxSW', 'TExSW', 'THDxSW']:
            return second_size_number * qty

    return 0


# # Definir la cantidad de soldaduras TW
def def_tw(row):
    face, type_code, diametric_welds, first_size_number, second_size_number, qty = row

    first_size_number = float(first_size_number)
    second_size_number = float(second_size_number)

    if type_code in ['SOL', 'WOL', 'LOL', 'THD']:
        return second_size_number*qty

    return 0


# Calcular pruebas radiográficas
def def_rt(row, ndt_dict):
    spec, bw, sw, tw = row

    total = bw*ndt_dict[spec]['BW']['RT'] + sw * \
        ndt_dict[spec]['SW']['RT'] + tw*ndt_dict[spec]['TW']['RT']

    return total


# Calcular tintas penetrantes
def def_lp(row, ndt_dict):
    spec, bw, sw, tw = row

    total = bw*ndt_dict[spec]['BW']['LP'] + sw * \
        ndt_dict[spec]['SW']['LP'] + tw*ndt_dict[spec]['TW']['LP']

    return total


def def_qty(row, rt_cell, rt_total, lp_cell, lp_total):
    description, qty = row

    if normalize_string(description) == rt_cell:
        return round(rt_total*1.2, 2)
    elif normalize_string(description) == lp_cell:
        return round(lp_total*1.2, 2)
    else:
        return qty


def ndt():
    # Leer el MTO limpio
    co_df = pd.read_csv('./output/mto.csv')

    # Obtener únicamente las columnas innecesarias
    co_df = co_df[['SPEC', 'LINE_NUM', 'TYPE', 'TYPE_CODE',
                   'FIRST_SIZE_NUMBER', 'SECOND_SIZE_NUMBER', 'FACE', 'QTY']]

    # Deajr únicamente las tuberías
    co_df = co_df[(co_df['TYPE'] == 'PP') | (
        co_df['TYPE'] == 'FT') | (co_df['TYPE'] == 'FL')]

    # Arreglar el segundo diámetro
    co_df['SECOND_SIZE_NUMBER'] = co_df[['TYPE', 'TYPE_CODE',
                                         'SECOND_SIZE_NUMBER']].apply(def_second_size_number, axis=1)

    # Ver la cantidad de solduras por cada elemento
    co_df['DIAMETRIC_WELDS'] = co_df[['TYPE', 'TYPE_CODE', 'FIRST_SIZE_NUMBER',
                                     'SECOND_SIZE_NUMBER', 'QTY', 'FACE']].apply(welds_per_element, axis=1)

    # Definir las soldaduras BW
    co_df['BW'] = co_df[['FACE', 'TYPE_CODE', 'DIAMETRIC_WELDS',
                         'FIRST_SIZE_NUMBER', 'SECOND_SIZE_NUMBER', 'QTY']].apply(def_bw, axis=1)

    # Definir las soldaduras SW
    co_df['SW'] = co_df[['FACE', 'TYPE_CODE', 'DIAMETRIC_WELDS',
                         'FIRST_SIZE_NUMBER', 'SECOND_SIZE_NUMBER', 'QTY']].apply(def_sw, axis=1)

    # Definir las soldaduras SW
    co_df['TW'] = co_df[['FACE', 'TYPE_CODE', 'DIAMETRIC_WELDS',
                         'FIRST_SIZE_NUMBER', 'SECOND_SIZE_NUMBER', 'QTY']].apply(def_tw, axis=1)

    # Se eliminan columnas innecesarias
    co_df.drop(['DIAMETRIC_WELDS'], inplace=True, axis=1)

    # Se crean las primeras listas de soldaduras
    welds_list_1 = co_df.groupby(['LINE_NUM', 'SPEC', 'TYPE', 'TYPE_CODE', 'FIRST_SIZE_NUMBER',
                                  'SECOND_SIZE_NUMBER', 'FACE'], as_index=False)[['QTY', 'BW', 'SW', 'TW']].agg(QTY=('QTY', sum), BW=('BW', sum), SW=('SW', sum), TW=('TW', sum))

    # Se crea la segunda lista de soldaduras
    welds_list_2 = welds_list_1.groupby(['LINE_NUM', 'SPEC'], as_index=False)[
        ['BW', 'SW', 'TW']].agg(BW=('BW', sum), SW=('SW', sum), TW=('TW', sum))

    # Se crea la tercera lista de soldaduras
    welds_list_3 = welds_list_2.groupby(['SPEC'], as_index=False)[
        ['BW', 'SW', 'TW']].agg(BW=('BW', sum), SW=('SW', sum), TW=('TW', sum))

    # Definir el porcentaje de ensayos por cada spec

    ndt_dict = {
        'CS2SA1': {
            'BW': {
                'RT': 1,
                'LP': 0
            },
            'SW': {
                'RT': 0,
                'LP': 1
            },
            'TW': {
                'RT': 0,
                'LP': 1
            }
        },
        'CS3SA1': {
            'BW': {
                'RT': 1,
                'LP': 0
            },
            'SW': {
                'RT': 0,
                'LP': 1
            },
            'TW': {
                'RT': 0,
                'LP': 1
            }
        },
        'CS4SA1': {
            'BW': {
                'RT': 1,
                'LP': 0
            },
            'SW': {
                'RT': 0,
                'LP': 1
            },
            'TW': {
                'RT': 0,
                'LP': 1
            }
        },
        'CS5SA1': {
            'BW': {
                'RT': 1,
                'LP': 0
            },
            'SW': {
                'RT': 0,
                'LP': 1
            },
            'TW': {
                'RT': 0,
                'LP': 1
            }
        },
        'CS6SA1': {
            'BW': {
                'RT': 1,
                'LP': 0
            },
            'SW': {
                'RT': 0,
                'LP': 1
            },
            'TW': {
                'RT': 0,
                'LP': 1
            }
        },
        'CS1SC2': {
            'BW': {
                'RT': 0.2,
                'LP': 0
            },
            'SW': {
                'RT': 0,
                'LP': 1
            },
            'TW': {
                'RT': 0,
                'LP': 1
            }
        }
    }

    welds_list_4 = welds_list_3.copy()

    # Definir las pruebas radiográficas
    welds_list_4['RT'] = welds_list_4[[
        'SPEC', 'BW', 'SW', 'TW']].apply(def_rt, axis=1, ndt_dict=ndt_dict)

    # Definir las tintas penetrantes
    welds_list_4['LP'] = welds_list_4[[
        'SPEC', 'BW', 'SW', 'TW']].apply(def_lp, axis=1, ndt_dict=ndt_dict)

    # Sumar todas las soldaduras
    rt_total = welds_list_4['RT'].sum()
    lp_total = welds_list_4['LP'].sum()

    # Ver en que celdas las agrego
    rt_cell = normalize_string('PRUEBAS RADIOGRAFICAS PARA JUNTA DE TUBERÍA')
    lp_cell = normalize_string(
        'PRUEBA DE TINTAS PENETRANTES PARA JUNTA DE TUBERÍA')

    # Leer el archivo de cantidades de obra creadas
    co_template = pd.read_csv('./output/co.csv')

    # Encontral la celda y colocar el valor
    co_template['QTY'] = co_template[[
        'DESCRIPTION', 'QTY']].apply(def_qty, axis=1, args=(rt_cell, rt_total, lp_cell, lp_total))

    # Guardar el archivo creado
    co_template.to_csv('./output/co.csv', index=False)
