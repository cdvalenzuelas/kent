from src.modules.co.co_temp import co_temp
from src.modules.co.supply import supply
from src.modules.co.pre_manufacturing import pre_manufacturing
from src.modules.co.valves_hidrostatic_test import valves_hidrostatic_test


def co():
    # Crear un archivo temporal que indique que items tienen información faltante em las cantidades de obra
    co_temp()

    # Definir el suministro
    supply()

    # Definir la prefabricación
    pre_manufacturing()

    # Definir las cantidades de pruebas hidrostáticas
    valves_hidrostatic_test()
