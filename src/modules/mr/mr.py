import pandas as pd


def mr():
    # Leer el archivo de summary
    mr_df = pd.read_csv('./output/summary.csv')

    # Filtrar el archivo y dejar sólo las válvulas
    mr_df = mr_df[mr_df['TYPE'] == 'VL']

    # Crear el archivo summary
    mr_df.to_csv('./output/mr.csv', index=True)
