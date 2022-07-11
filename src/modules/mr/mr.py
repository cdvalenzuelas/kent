import pandas as pd


def mr(summary_df):
    # Hacer una copia del summary_df
    summary_df = summary_df.copy()

    # Filtrar el archivo y dejar sólo las válvulas
    mr_df = summary_df[summary_df['TYPE'] == 'VL']

    mr_df.reset_index(inplace=True)

    # Crear el archivo summary
    return mr_df
