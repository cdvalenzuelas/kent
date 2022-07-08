import pandas as pd

from src.modules.compare_pid.line_diferences import line_diferences
from src.modules.compare_pid.valves_diferences import valves_diferences


def compare_pid(mto_df):
    # Hacer una copia del df
    mto_df = mto_df.copy()

    # Leer el archivo de P&ID
    pid_df = pd.read_csv('./inputs/p&id.csv')

    # Dejar únicamente las columnas necesarias del MTO
    mto_df.drop(['DESCRIPTION', 'SECOND_SIZE_NUMBER',
                'SCH', 'FACE', 'UNITS', 'WEIGHT_PER_UNIT', 'TOTAL_WEIGHT'], inplace=True, axis=1)

    # Ver las diferencias entre las líneas del BOM y las líneas del P&D
    bom_lines_unique, pid_lines_unique = line_diferences(mto_df, pid_df)

    # Comparar las válvulas
    valves_diferences(bom_lines_unique, pid_lines_unique, mto_df, pid_df)
