import shutil
import os

from src.modules.mto_exist.mto_exist import mto_exist
from src.modules.mto_does_not_exist import mto_does_not_exist
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

    # Definir si nos entregan MTO o BOM
    mto_already_exist = False

    # Definir el cliente
    client = 'cenit'

    # Se crea el MTO en función de si entregan un MTO hecho o un BOM desde 0
    if not mto_already_exist:
        # Entregan un BOM desde 0
        mto_does_not_exist()
    else:
        # Nos entregan el MTO hecho para hacer correcciones
        mto_exist()

    # Se crea la HD
    # hd()

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
