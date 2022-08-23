import pandas as pd


def mr(summary_df):
    # (VALEC17) Hacer una copia del summary_df
    summary_df = summary_df.copy()

    # (VALEC17) Filtrar el archivo y dejar sólo las válvulas
    mr_df = summary_df[summary_df['TYPE'] == 'VL']

    mr_df.reset_index(inplace=True)

    # (VALEC17) Crear el archivo summary
    return mr_df
