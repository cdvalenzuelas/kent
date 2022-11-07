import pandas as pd
import numpy as np


def delete_empty_columns_and_rows(bom_df, cad_software):
    # (VALEC17) HACER UNA COPIA DEL BOM
    bom_df = bom_df.copy()

    # (VALEC17) Recoger las columnas que no se encuetran nombradas
    valid_columns = [
        column for column in bom_df.columns if str(column) != 'nan']

    # (VALEC17) Eliminar las columnas que no se encuetran nombradas
    bom_df = bom_df[valid_columns]

    # (VALEC17) Definir si las filas son vacías o no
    def def_na(row, columns):
        cond = True

        for column in columns:
            if str(row[column]) != 'nan':
                cond = False
                break

        return cond

    # (VALEC17) Definir si las filas son vacías o no
    bom_df['NA'] = bom_df.apply(def_na, axis=1, columns=bom_df.columns)

    # (VALEC17) Eliminar las filas vacías
    bom_df = bom_df[(bom_df['NA'] == False)]

    # (VALEC17) Eliminar las columnas innecesarias
    bom_df.drop(['NA'], axis=1, inplace=True)

    # (VALEC17) Lenar campos vacíos
    if cad_software == 'autoplant':
        bom_df['PESO TOTAL'].fillna(0, inplace=True)
        bom_df['PESO'].fillna(0, inplace=True)
        bom_df['PESO TOTAL'] = bom_df['PESO TOTAL'].str.replace(',', '')
    elif cad_software == 'cadworks':
        bom_df['WEIGHT'].fillna(0, inplace=True)

    bom_df.fillna('-', inplace=True)

    # (VALEC17) Retornar el bom_df sin columnas ni filas cacías
    return bom_df
