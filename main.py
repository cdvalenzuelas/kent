import shutil
import os

from src.modules.transform_bom import transform_bom
from src.modules.mto import mto
from src.modules.summary.summary import summary
from src.modules.mr.mr import mr
from src.modules.hd.hd import hd
from src.modules.co.co import co
from src.modules.compare_pid.compare_pid import compare_pid
from src.utils.clean_csv import clean_csv

# (VALEC17) Piping classes
from src.clients.cenit.piping_class.cenit_piping_class import cenit_piping_class


if __name__ == '__main__':
    # (VALEC17) Eliminar los archivos de la carpeta output
    try:
        shutil.rmtree('output')

        os.mkdir('output')
    except:
        pass

    # (VALEC17) Eliminar los archivos de la carpeta diacnostic
    try:
        shutil.rmtree('diacnostic')

        os.mkdir('diacnostic')
    except:
        pass

    # (VALEC17) Definir el cliente
    client = 'cenit'

    # (VALEC17) Definir si se usarán los pesos de válvulas de bom o de piping class
    piping_class_valves_weights = True

    # (VALEC17) Definir el piping class a utilizar (puede ser un llamado a una base de datos)
    piping_class = None

    if client == 'cenit':
        piping_class = cenit_piping_class()

    # (VALEC17) Se trensforma el bom a un formato standard sin importar el programa de diseño utilizado
    (bom_is_correct, bom_df) = transform_bom(piping_class)

    # (VALEC17) CREAR EL ARCHIVO DE BOM ARREGLADO
    bom_df.to_excel('./inputs/bom_fixed.xlsx', index=False)

    # (VALEC17) Si se reconoce algún
    if bom_is_correct:
        # (VALEC17) Se crea el MTO
        (mto_df, mto_df_for_co) = mto(
            bom_df, piping_class, piping_class_valves_weights)

        # (VALEC17) Comparar con la info del P&ID con el MTO
        mto_df = compare_pid(mto_df)

        # (VALEC17) Se crea la HD
        hd(mto_df)

        # (VALEC17) Se crean las cantidades de obra
        co_df = co(client, mto_df_for_co, piping_class)

        # (VALEC17) Creación del sumario
        summary_df = summary(mto_df)

        # (VALEC17) Se crea el MR
        mr_df = mr(summary_df)

        # (VALEC17) Se limpian los archivos crados
        clean_csv(mto_df, summary_df, mr_df, co_df)
