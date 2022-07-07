import pandas as pd

from src.utils.normalize_string import normalize_string
from src.clients.cenit.co.ndt.welds_per_element import welds_per_element
from src.clients.cenit.co.ndt.def_bw import def_bw
from src.clients.cenit.co.ndt.def_sw import def_sw
from src.clients.cenit.co.ndt.def_tw import def_tw
from src.clients.cenit.co.ndt.def_rt import def_rt
from src.clients.cenit.co.ndt.def_lp import def_lp
from src.clients.cenit.co.ndt.ndt_level import ndt_level
from src.clients.cenit.co.ndt.def_qty import def_qty


# Coloca el segundo diámetro corecto (elimina basura)
def def_second_size_number(row):
    type_element, type_code, second_size_number = row

    if second_size_number == '-':
        return 0

    if type_code == 'NIP':
        return 0

    return second_size_number


def ndt():
    # Leer el MTO limpio
    co_df = pd.read_csv('./output/mto.csv')

    # Obtener únicamente las columnas innecesarias
    co_df = co_df[['SPEC', 'LINE_NUM', 'TYPE', 'TYPE_CODE',
                   'FIRST_SIZE_NUMBER', 'SECOND_SIZE_NUMBER', 'FACE', 'QTY']]

    # Deajr únicamente las tuberías
    co_df = co_df[(co_df['TYPE'] == 'PP') | (
        co_df['TYPE'] == 'FT') | (co_df['TYPE'] == 'FL')]

    # Si existen tuberpias y/o accesorios
    if co_df.shape[0] > 0:

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

        welds_list_4 = welds_list_3.copy()

        # Definir las pruebas radiográficas
        welds_list_4['RT'] = welds_list_4[[
            'SPEC', 'BW', 'SW', 'TW']].apply(def_rt, axis=1, ndt_dict=ndt_level)

        # Definir las tintas penetrantes
        welds_list_4['LP'] = welds_list_4[[
            'SPEC', 'BW', 'SW', 'TW']].apply(def_lp, axis=1, ndt_dict=ndt_level)

        # Sumar todas las soldaduras
        rt_total = welds_list_4['RT'].sum()
        lp_total = welds_list_4['LP'].sum()

        # Ver en que celdas las agrego
        rt_cell = normalize_string(
            'PRUEBAS RADIOGRAFICAS PARA JUNTA DE TUBERÍA')
        lp_cell = normalize_string(
            'PRUEBA DE TINTAS PENETRANTES PARA JUNTA DE TUBERÍA')

        # Leer el archivo de cantidades de obra creadas
        co_template = pd.read_csv('./output/co.csv')

        # Encontral la celda y colocar el valor
        co_template['QTY'] = co_template[[
            'DESCRIPTION', 'QTY']].apply(def_qty, axis=1, args=(rt_cell, rt_total, lp_cell, lp_total))

        # Guardar el archivo creado
        co_template.to_csv('./output/co.csv', index=False)
