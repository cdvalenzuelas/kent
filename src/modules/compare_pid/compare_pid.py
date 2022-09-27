import pandas as pd

from src.modules.compare_pid.line_diferences import line_diferences
from src.modules.compare_pid.valves_diferences.valves_diferences import valves_diferences
from src.modules.compare_pid.locking_device import locking_device
from src.modules.compare_pid.cleaner import cleaner
from src.modules.compare_pid.elements_difference.elements_difference import elements_difference


def compare_pid(mto_df):
    # (VALEC17) Hacer una copia del df
    mto_df = mto_df.copy()

    # (VALEC17) Aquí hay un limpiador que devuelve un archivo agrupado, con cantidades y con tags asiganos (aquí se le pregunta al usaurio en caso de que hayan más válvulas)
    pid_df = cleaner()

    # (VALEC17) Ver las diferencias entre las líneas del BOM y las líneas del P&D
    line_diferences(mto_df, pid_df)

    # (VALEC17) Comparar las válvulas
    #valves_diferences(mto_df, pid_df)

    # (VALEC17) Buscar una diferencia entre el P&ID y el MTO
    elements_difference(mto_df, pid_df)

    # (VALEC17) Modificar en el MTO, SUMARIO, MR y HD las válulas que cuenten con locking device
    mto_df = locking_device(mto_df, pid_df)

    return mto_df
