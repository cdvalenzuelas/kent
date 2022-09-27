import pandas as pd


from src.modules.compare_pid.search_valve_tag import search_valve_tag


def cleaner():
    # (VALEC17) Leer el archivo de P&ID
    pid_df = pd.read_csv('./inputs/p&id.csv')

    # (VALEC17) Rellenar las cantidades vacías con ceros
    pid_df['SECOND_SIZE_NUMBER'].fillna('-', inplace=True)
    pid_df['TAG'].fillna('-', inplace=True)
    pid_df['CSO'].fillna(0, inplace=True)
    pid_df['CSC'].fillna(0, inplace=True)
    pid_df['NO_LOCKING_DEVICE'].fillna(0, inplace=True)

    # (VALEC17) Llenar los espacios vacíos con '-'
    pid_df.fillna('-', inplace=True)

    # (VALEC17) Sumar el pid_df
    pid_df = pid_df.groupby(['LINE_NUM', 'SPEC', 'TYPE_CODE', 'FIRST_SIZE_NUMBER', 'SECOND_SIZE_NUMBER', 'TAG'], as_index=False)[['CSO', 'CSC', 'NO_LOCKING_DEVICE']].agg(
        CSO=('CSO', sum),
        CSC=('CSC', sum),
        NO_LOCKING_DEVICE=('NO_LOCKING_DEVICE', sum))

    # (VALEC17) Sumar la cantidad
    pid_df['QTY'] = pid_df['CSO'] + pid_df['CSC'] + pid_df['NO_LOCKING_DEVICE']

    return pid_df
