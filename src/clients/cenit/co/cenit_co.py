import pandas as pd

from src.clients.cenit.co.co_temp import co_temp
from src.clients.cenit.co.demolition.demolition import demolition
from src.clients.cenit.co.supply.supply import supply
from src.clients.cenit.co.pre_manufacturing.pre_manufacturing import pre_manufacturing
from src.clients.cenit.co.valves_hidrostatic_test.valves_hidrostatic_test import valves_hidrostatic_test
from src.clients.cenit.co.erection.erection import erection
from src.clients.cenit.co.areas.areas import areas
from src.clients.cenit.co.pipes_hisdrostatic_test.pipes_hidrostatic_test import pipes_hidrostatic_test
from src.clients.cenit.co.ndt.ndt import ndt
from src.clients.cenit.co.valves_tags.valves_tags import valves_tags
from src.clients.cenit.co.distance.distance import distance


def cenit_co(cenit_co_conf, mto_df, piping_class):
    # (VALEC17) Hacer una copia del mto_df
    mto_df = mto_df.copy()

    # (VALEC17) Crear un archivo temporal que indique que items tienen información faltante em las cantidades de obra
    co_temp(mto_df)

    # (VALEC17) Leer el template de CO
    co_df = pd.read_csv('./src/clients/cenit/templates/co_template.csv')

    # (VALEC17) Definir el suministro
    if cenit_co_conf['supply']:
        co_df = supply(mto_df, co_df)

    # (VALEC17) Definir la prefabricación
    if cenit_co_conf['pre_manufacturing']:
        co_df = pre_manufacturing(mto_df, co_df)

    # (VALEC17) Definir las cantidades de pruebas hidrostáticas
    if cenit_co_conf['valves_hidrostatic_test']:
        co_df = valves_hidrostatic_test(mto_df, co_df)

    # (VALEC17) Definir el montaje
    if cenit_co_conf['erection']:
        co_df = erection(mto_df, co_df)

    # (VALEC17) Definir áreas
    if cenit_co_conf['areas']:
        co_df = areas(mto_df, co_df)

    # (VALEC17) Definir las pruebas hidrostáticas sobre la tubería
    if cenit_co_conf['pipes_hidrostatic_test']:
        co_df = pipes_hidrostatic_test(mto_df, co_df)

    # (VALEC17) Definir soldaduras
    if cenit_co_conf['ndt']:
        co_df = ndt(mto_df, co_df)

    # (VALEC17) Definir el desmantelamiento
    if cenit_co_conf['demolition']['demolition']:
        co_df = demolition(
            cenit_co_conf['demolition']['method'], co_df, piping_class)

    # (VALEC17) Definir la demarcación de válvulas (sólo cuenta válvulas y no tuberías)
    if cenit_co_conf['valves_tags']:
        co_df = valves_tags(mto_df, co_df)

    co_df = distance(cenit_co_conf['messure'], mto_df, co_df)

    return co_df
