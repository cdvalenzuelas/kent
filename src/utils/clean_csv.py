from os import PRIO_PGRP
import pandas as pd

from src.utils.replace_dot_by_comma import replace_dot_by_comma


def df_round(row):
    data, spec = row

    return round(data, 4)


def clean_csv(mto_df, summary_df, mr_df, co_df):
    # (VALEC17) Hacer copias de lod df
    mto_df = mto_df.copy()
    summary_df = summary_df.copy()
    mr_df = mr_df.copy()
    co_df = co_df.copy()

    # (VALEC17) Ordenar los dataframes
    summary_df.sort_values(by=['ORDER', 'TYPE_CODE', 'FIRST_SIZE_NUMBER',
                               'SECOND_SIZE_NUMBER', 'SCH', 'FACE', 'RATING', 'TAG', 'NOTE'], inplace=True)

    summary_df.reset_index(inplace=True)

    mto_df.sort_values(by=['LINE_NUM', 'SPEC', 'ORDER', 'TYPE_CODE', 'FIRST_SIZE_NUMBER',
                           'SECOND_SIZE_NUMBER', 'SCH', 'FACE', 'RATING', 'TAG', 'NOTE'], inplace=True)
    mto_df.reset_index(inplace=True)

    mr_df.sort_values(by=['TAG', 'FIRST_SIZE_NUMBER', 'NOTE'], inplace=True)

    mr_df.reset_index(inplace=True)

    # (VALEC17) Dejar únicamente las columnas necesarias
    mr_df = mr_df[['Catalogacion', 'TAG', 'DESCRIPTION',
                   'FIRST_SIZE_NUMBER', 'QTY', 'UNITS', 'NOTE']]

    summary_df = summary_df[['Catalogacion', 'TYPE', 'TYPE_CODE', 'DESCRIPTION', 'FIRST_SIZE_NUMBER',
                             'SECOND_SIZE_NUMBER', 'SCH', 'FACE', 'RATING', 'QTY', 'UNITS', 'WEIGHT_PER_UNIT', 'TOTAL_WEIGHT', 'NOTE']]

    mto_df = mto_df[['Catalogacion', 'LINE_NUM', 'SPEC', 'TYPE', 'TYPE_CODE', 'DESCRIPTION', 'FIRST_SIZE_NUMBER',
                     'SECOND_SIZE_NUMBER', 'SCH', 'FACE', 'RATING', 'QTY', 'UNITS', 'WEIGHT_PER_UNIT', 'TOTAL_WEIGHT', 'NOTE']]

    # (VALEC17) Renombrar columnas
    mr_df.rename(
        columns={'TAG': 'CODE', 'FIRST_SIZE_NUMBER': 'NOMINAL_SIZE'}, inplace=True)

    # (VALEC17) Redondeando los listados
    mto_df['TOTAL_WEIGHT'] = mto_df[[
        'TOTAL_WEIGHT', 'SPEC']].apply(df_round, axis=1)
    mto_df['WEIGHT_PER_UNIT'] = mto_df[[
        'WEIGHT_PER_UNIT', 'SPEC']].apply(df_round, axis=1)

    summary_df['TOTAL_WEIGHT'] = summary_df[[
        'TOTAL_WEIGHT', 'TYPE']].apply(df_round, axis=1)
    summary_df['WEIGHT_PER_UNIT'] = summary_df[['WEIGHT_PER_UNIT', 'TYPE']].apply(
        df_round, axis=1)

    co_df['QTY'] = co_df[['QTY', 'CODE']].apply(df_round, axis=1)

    # (VALEC17) Cambiar puntos por comas en todos los archivos de salida
    mto_df['FIRST_SIZE_NUMBER'] = mto_df['FIRST_SIZE_NUMBER'].apply(
        replace_dot_by_comma)
    mto_df['SECOND_SIZE_NUMBER'] = mto_df['SECOND_SIZE_NUMBER'].apply(
        replace_dot_by_comma)
    mto_df['WEIGHT_PER_UNIT'] = mto_df['WEIGHT_PER_UNIT'].apply(
        replace_dot_by_comma)
    mto_df['TOTAL_WEIGHT'] = mto_df['TOTAL_WEIGHT'].apply(replace_dot_by_comma)

    summary_df['FIRST_SIZE_NUMBER'] = summary_df['FIRST_SIZE_NUMBER'].apply(
        replace_dot_by_comma)
    summary_df['SECOND_SIZE_NUMBER'] = summary_df['SECOND_SIZE_NUMBER'].apply(
        replace_dot_by_comma)
    summary_df['WEIGHT_PER_UNIT'] = summary_df['WEIGHT_PER_UNIT'].apply(
        replace_dot_by_comma)
    summary_df['TOTAL_WEIGHT'] = summary_df['TOTAL_WEIGHT'].apply(
        replace_dot_by_comma)

    mr_df['QTY'] = mr_df['QTY'].apply(replace_dot_by_comma)
    mr_df['NOMINAL_SIZE'] = mr_df['NOMINAL_SIZE'].apply(replace_dot_by_comma)

    co_df['QTY'] = co_df['QTY'].apply(
        replace_dot_by_comma)

    # (VALEC17) Poner una columna de items (numeración en cada documento)
    item = pd.DataFrame({'ITEM': list(range(1, mr_df.shape[0] + 1))})
    mr_df = pd.concat([item, mr_df], axis=1)

    item = pd.DataFrame({'ITEM': list(range(1, summary_df.shape[0] + 1))})
    summary_df = pd.concat([item, summary_df], axis=1)

    item = pd.DataFrame({'ITEM': list(range(1, mto_df.shape[0] + 1))})
    mto_df = pd.concat([item, mto_df], axis=1)

    # (VALEC17) Crear el archivos
    mr_df.to_excel('./output/mr.xlsx', index=False)
    summary_df.to_excel('./output/summary.xlsx', index=False)
    mto_df.to_excel('./output/mto.xlsx', index=False)
    co_df.to_excel('./output/co.xlsx', index=False)
