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

# Piping classes
from src.clients.cenit.piping_class.cenit_piping_class import cenit_piping_class


if __name__ == '__main__':
    # Eliminar los archivos de la carpeta output
    try:
        shutil.rmtree('output')

        os.mkdir('output')
    except:
        pass

    # Definir el cliente
    client = 'cenit'

    # Definir si se usarán los pesos de válvulas de bom o de piping class
    piping_class_valves_weights = True

    # Definir el piping class a utilizar (puede ser un llamado a una base de datos)
    piping_class = None

    if client == 'cenit':
        piping_class = cenit_piping_class()

    # Se trensforma el bom a un formato standard sin importar el programa de diseño utilizado
    (bom_is_correct, bom_df) = transform_bom()

    # Si se reconoce algún
    if bom_is_correct:
        # Se crea el MTO
        mto_df = mto(bom_df, piping_class, piping_class_valves_weights)

        # Comparar con la info del P&ID con el MTO
        mto_df = compare_pid(mto_df, piping_class)

        # Se crea la HD
        hd(mto_df)

        # Se crean las cantidades de obra
        co_df = co(client, mto_df, piping_class)

        # Creación del sumario
        summary_df = summary(mto_df)

        # Se crea el MR
        mr_df = mr(summary_df)

        # Se limpian los archivos crados
        clean_csv(mto_df, summary_df, mr_df, co_df)
