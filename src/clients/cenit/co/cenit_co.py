from src.clients.cenit.co.co_temp import co_temp
from src.clients.cenit.co.demolition import demolition
from src.clients.cenit.co.supply import supply
from src.clients.cenit.co.pre_manufacturing import pre_manufacturing
from src.clients.cenit.co.valves_hidrostatic_test import valves_hidrostatic_test
from src.clients.cenit.co.erection import erection
from src.clients.cenit.co.areas import areas
from src.clients.cenit.co.pipes_hidrostatic_test import pipes_hidrostatic_test
from src.clients.cenit.co.ndt.ndt import ndt
from src.clients.cenit.co.valves_tags import valves_tags
from src.clients.cenit.co.distance import distance


def cenit_co(cenit_co_conf):
    # Crear un archivo temporal que indique que items tienen información faltante em las cantidades de obra
    co_temp()

    # Definir el suministro
    if cenit_co_conf['supply']:
        supply()

    # Definir la prefabricación
    if cenit_co_conf['pre_manufacturing']:
        pre_manufacturing()

    # Definir las cantidades de pruebas hidrostáticas
    if cenit_co_conf['valves_hidrostatic_test']:
        valves_hidrostatic_test()

    # Definir el montaje
    if cenit_co_conf['erection']:
        erection()

    # Definir áreas
    if cenit_co_conf['areas']:
        areas()

    # Definir las pruebas hidrostáticas sobre la tubería
    if cenit_co_conf['pipes_hidrostatic_test']:
        pipes_hidrostatic_test()

    # Definir soldaduras
    if cenit_co_conf['ndt']:
        ndt()

    # Definir el desmantelamiento
    if cenit_co_conf['demolition']['demolition']:
        demolition(cenit_co_conf['demolition']['method'])

    # Definir la demarcación de válvulas (sólo cuenta válvulas y no tuberías)
    if cenit_co_conf['valves_tags']:
        valves_tags()

    distance(cenit_co_conf['messure'])
