import pandas as pd

from src.modules.transform_bom.delete_empty_columns_and_rows import delete_empty_columns_and_rows
from src.modules.transform_bom.reorganize_columns import reorganize_columns
from src.modules.transform_bom.search_type_code import search_type_code
from src.modules.transform_bom.search_tag import search_tag
from src.modules.transform_bom.autoplant import autoplant
from src.modules.transform_bom.smartplant import smartplant


def transform_bom(piping_class):
    # (VALEC17) REORGANIZE COLUMNS
    bom_df, cad_software = reorganize_columns()

    # (VALEC17) Generando DF sin columnas y filas vacías
    bom_df = delete_empty_columns_and_rows(bom_df, cad_software)

    # (VALEC17) Buscar el type Code
    bom_df = search_type_code(bom_df, cad_software)

    if cad_software == 'cadworks':
        bom_df = search_tag(bom_df, piping_class)
        return (True, bom_df)
    elif cad_software == 'autoplant':
        bom_df = autoplant(bom_df)
        bom_df = search_tag(bom_df, piping_class)
        return (True, bom_df)
    elif cad_software == 'smartplant':
        bom_df = smartplant(bom_df, piping_class)
        bom_df = search_tag(bom_df, piping_class)
        return (True, bom_df)
    else:
        print('\n❌ NO SE RECONOCE EL PROGRAMA DE DISEÑO, LAS COLUMNAS DEL BOM NO CORRESPONDEN A NINGUN TEMPLATE ESTABLECIDO')
        return False
