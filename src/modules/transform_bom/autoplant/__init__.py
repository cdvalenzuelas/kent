import pandas as pd

from src.modules.transform_bom.autoplant.def_lenght import def_lenght
from src.modules.transform_bom.autoplant.def_qty import def_qty
from src.modules.transform_bom.autoplant.def_main_size import def_main_size
from src.modules.transform_bom.autoplant.def_red_size import def_red_size

# (VALEC17) PASAR DE CADWORKS A CADWORKS


def autoplant(bom_df):
    # (VALEC17) Hacer una copia del df
    bom_df = bom_df.copy()

    # (VALEC17) Agregando columnas adicionaels
    bom_df['MARK'] = bom_df['ITEM']
    bom_df['LINE_NUM'] = bom_df['LINE NUMBER']
    bom_df['SPEC_FILE'] = bom_df['SPEC']
    bom_df['DB_CODE'] = bom_df['STYPE']
    bom_df['DESCRIPTION'] = bom_df['COMPONENT DESCRIPTION']
    bom_df['SHORT_DESC'] = bom_df['COMPONENT DESCRIPTION']
    bom_df['MAIN_NOM'] = '-'
    bom_df['RED_NOM'] = '-'
    bom_df['THK_NOM'] = '-'
    bom_df['QTY'] = bom_df['QUANTITY']
    bom_df['TAG'] = '-'
    bom_df['LENGTH'] = 0
    bom_df['WEIGHT'] = bom_df['PESO TOTAL']

    # (VALEC17) RELLENAR LOS PESOS INEXISTENTES CON CERO
    bom_df['WEIGHT'] = bom_df['WEIGHT'].str.replace('-', '0')

    # (VALEC17) Eliminar columnas
    bom_df.drop(columns=['ITEM', 'LINE NUMBER', 'SPEC', 'STYPE', 'COMPONENT DESCRIPTION', 'PESO',
                'PESO TOTAL', 'GTYPE', 'SCHEDULE', 'RATING', 'FACING', 'QUANTITY', 'UNITS'], inplace=True)

    # (VALEC17) Reorganizar columnas
    bom_df = bom_df[['MARK', 'LINE_NUM', 'SPEC_FILE', 'DB_CODE', 'DESCRIPTION', 'SHORT_DESC',
                    'SIZE', 'MAIN_NOM', 'RED_NOM', 'THK_NOM', 'QTY', 'TAG', 'LENGTH', 'WEIGHT']]

    # (VALEC17) DEFINIR LA LONGITUD DE LOS ELEMENTOS
    bom_df['LENGTH'] = bom_df[['DB_CODE', 'QTY',
                               'SIZE', 'SHORT_DESC']].apply(def_lenght, axis=1)

    # (VALEC17) DEFINIR LAS CANTIDADES DE LOS ELEMENTOS
    bom_df['QTY'] = bom_df[['DB_CODE', 'QTY']].apply(def_qty, axis=1)

    # (VALEC17) DEFINIR EL TAMAÑO PRINCIPAL
    bom_df['MAIN_NOM'] = bom_df[['DB_CODE', 'SIZE']].apply(
        def_main_size, axis=1)

    # (VALEC17) DEFINIR EL TAMAÑO SECUNDARIO
    bom_df['RED_NOM'] = bom_df[['DB_CODE', 'SIZE']].apply(def_red_size, axis=1)

    return bom_df
