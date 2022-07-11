import pandas as pd


from src.modules.compare_pid.search_valve_tag import search_valve_tag


def cleaner(piping_class):
    # Leer el archivo de P&ID
    pid_df = pd.read_csv('./inputs/p&id.csv')

    # Rellenar las cantidades vacías con ceros
    pid_df['CSO'].fillna(0, inplace=True)
    pid_df['CSC'].fillna(0, inplace=True)
    pid_df['NO_LOCKING_DEVICE'].fillna(0, inplace=True)

    # Sumar el pid_df
    pid_df = pid_df.groupby(['LINE_NUM', 'SPEC', 'TYPE_CODE', 'FIRST_SIZE_NUMBER', 'RATING'], as_index=False)[['CSO', 'CSC', 'NO_LOCKING_DEVICE']].agg(
        CSO=('CSO', sum),
        CSC=('CSC', sum),
        NO_LOCKING_DEVICE=('NO_LOCKING_DEVICE', sum))

    # Sumar la cantidad
    pid_df['QTY'] = pid_df['CSO'] + pid_df['CSC'] + pid_df['NO_LOCKING_DEVICE']

    # Buscar el tag de las válvulas
    pid_df = search_valve_tag(pid_df, piping_class)

    return pid_df
