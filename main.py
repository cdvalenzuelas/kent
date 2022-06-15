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


if __name__ == '__main__':
    # Eliminar los archivos de la carpeta output
    try:
        shutil.rmtree('output')

        os.mkdir('output')
    except:
        pass

    # Definir el cliente
    client = 'cenit'

    # Se trensforma el bom a un formato standard sin importar el programa de diseño utilizado
    bom_is_correct = transform_bom()

    # Si se reconoce algún
    if bom_is_correct:
        # Se crea el MTO
        mto()

        # Se crea la HD
        hd()

        # Se crean las cantidades de obra
        co(client)

        # Creación del sumario
        summary()

        # Se crea el MR
        mr()

        # Se limpian los archivos crados
        clean_csv()

        # Comparar con la info del P&ID con el MTO
        compare_pid()
