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


# (VALEC17) Coloca el segundo diámetro corecto (elimina basura)
def def_second_size_number(row):
    type_element, type_code, second_size_number = row

    if second_size_number == '-':
        return 0

    if type_code == 'NIP':
        return 0

    return second_size_number


def ndt(mto_df, co_df):
    # (VALEC17) Obtener únicamente las columnas innecesarias
    mto_df = mto_df[['SPEC', 'TYPE', 'TYPE_CODE',
                     'FIRST_SIZE_NUMBER', 'SECOND_SIZE_NUMBER', 'QTY', 'FACE']]

    # (VALEC17) Deajr únicamente las tuberías y accesorios
    mto_df = mto_df[(mto_df['TYPE'] == 'PP') | (
        mto_df['TYPE'] == 'FT') | (mto_df['TYPE'] == 'FL')]

    # (VALEC17) Si existen tuberpias y/o accesorios
    if mto_df.shape[0] > 0:

        # (VALEC17) Arreglar el segundo diámetro
        mto_df['SECOND_SIZE_NUMBER'] = mto_df[['TYPE', 'TYPE_CODE',
                                               'SECOND_SIZE_NUMBER']].apply(def_second_size_number, axis=1)

        # (VALEC17) Ver la cantidad de solduras por cada elemento
        mto_df['DIAMETRIC_WELDS'] = mto_df[['TYPE', 'TYPE_CODE', 'FIRST_SIZE_NUMBER',
                                            'SECOND_SIZE_NUMBER', 'QTY']].apply(welds_per_element, axis=1)

        # (VALEC17) Definir las soldaduras BW
        mto_df['BW'] = mto_df[['FACE', 'TYPE_CODE', 'DIAMETRIC_WELDS',
                               'FIRST_SIZE_NUMBER', 'SECOND_SIZE_NUMBER', 'QTY']].apply(def_bw, axis=1)

        # (VALEC17) Definir las soldaduras SW
        mto_df['SW'] = mto_df[['FACE', 'TYPE_CODE', 'DIAMETRIC_WELDS',
                               'FIRST_SIZE_NUMBER', 'SECOND_SIZE_NUMBER', 'QTY']].apply(def_sw, axis=1)

        # (VALEC17) Definir las soldaduras SW
        mto_df['TW'] = mto_df[['FACE', 'TYPE_CODE', 'DIAMETRIC_WELDS',
                               'FIRST_SIZE_NUMBER', 'SECOND_SIZE_NUMBER', 'QTY']].apply(def_tw, axis=1)

        # (VALEC17) Se eliminan columnas innecesarias
        mto_df.drop(['DIAMETRIC_WELDS'], inplace=True, axis=1)

        # (VALEC17) Se crean las primeras listas de soldaduras
        welds_list_1 = mto_df.groupby(['SPEC', 'TYPE', 'TYPE_CODE', 'FIRST_SIZE_NUMBER',
                                      'SECOND_SIZE_NUMBER', 'FACE'], as_index=False)[['QTY', 'BW', 'SW', 'TW']].agg(QTY=('QTY', sum), BW=('BW', sum), SW=('SW', sum), TW=('TW', sum))

        # (VALEC17) Se crea la segunda lista de soldaduras
        welds_list_2 = welds_list_1.groupby(['SPEC'], as_index=False)[
            ['BW', 'SW', 'TW']].agg(BW=('BW', sum), SW=('SW', sum), TW=('TW', sum))

        # (VALEC17) Definir el porcentaje de ensayos por cada spec
        welds_list_3 = welds_list_2.copy()

        # (VALEC17) Definir las pruebas radiográficas
        welds_list_3['RT'] = welds_list_3[[
            'SPEC', 'BW', 'SW', 'TW']].apply(def_rt, axis=1, ndt_dict=ndt_level)

        # (VALEC17) Definir las tintas penetrantes
        welds_list_3['LP'] = welds_list_3[[
            'SPEC', 'BW', 'SW', 'TW']].apply(def_lp, axis=1, ndt_dict=ndt_level)

        # (VALEC17) Sumar todas las soldaduras
        rt_total = welds_list_3['RT'].sum()
        lp_total = welds_list_3['LP'].sum()

        # (VALEC17) Ver en que celdas las agrego
        rt_cell = normalize_string(
            'PRUEBAS RADIOGRAFICAS PARA JUNTA DE TUBERÍA')
        lp_cell = normalize_string(
            'PRUEBA DE TINTAS PENETRANTES PARA JUNTA DE TUBERÍA')

        # (VALEC17) Encontral la celda y colocar el valor
        co_df['QTY'] = co_df[[
            'DESCRIPTION', 'QTY']].apply(def_qty, axis=1, args=(rt_cell, rt_total, lp_cell, lp_total))

    # (VALEC17) Guardar el archivo creado
    return co_df
