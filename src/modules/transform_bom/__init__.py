import pandas as pd

from src.modules.transform_bom.delete_empty_columns_and_rows import delete_empty_columns_and_rows
from src.modules.transform_bom.detect_cad_software import detect_cad_software
from src.modules.transform_bom.transform_autoplant_to_cadworks import transform_autoplant_to_cadworks


def transform_bom():
    # Generando DF sin columnas y filas vacías
    bom_df = delete_empty_columns_and_rows()

    # Detectar softaware
    cad_software = detect_cad_software(bom_df)

    if cad_software == 'cadworks':
        bom_df.to_csv('./inputs/bom.csv', index=False)
        return True
    elif cad_software == 'autoplant':
        transform_autoplant_to_cadworks(bom_df)
        return True
    else:
        print('\n❌ NO SE RECONOCE EL PROGRAMA DE DISEÑO, LAS COLUMNAS DEL BOM NO CORRESPONDEN A NINGUN TEMPLATE ESTABLECIDO')
        return False
