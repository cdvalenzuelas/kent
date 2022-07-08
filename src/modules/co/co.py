# Se traen las cantidades de obra de cada cliente
from src.clients.cenit.co.cenit_co import cenit_co


# Se traen los archivos de configuración para cada cliente
from src.clients.cenit.co.cenit_co_conf import cenit_co_conf


# Esta función define que cliente se está trabajando y ejecuta sus cantidades de obra
def co(client, mto_df):
    print(
        f'💡 RECUERDE MODIFICAR EL ARCHIVO DE CONFIGUARACIÓN DE CANTIDADES DE OBRA DE {client.upper()}\n')

    # Ejecutar cada cantidad de obra con su archivo de configuración
    if client == 'cenit':
        return cenit_co(cenit_co_conf, mto_df)
