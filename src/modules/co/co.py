# (VALEC17) Se traen las cantidades de obra de cada cliente
from src.clients.cenit.co.cenit_co import cenit_co


# (VALEC17) Se traen los archivos de configuración para cada cliente
from src.clients.cenit.co.cenit_co_conf import cenit_co_conf


# (VALEC17) Esta función define que cliente se está trabajando y ejecuta sus cantidades de obra
def co(client, mto_df, piping_class):
    print(
        f'💡 RECUERDE MODIFICAR EL ARCHIVO DE CONFIGUARACIÓN DE CANTIDADES DE OBRA DE {client.upper()}\n')

    # (VALEC17) Ejecutar cada cantidad de obra con su archivo de configuración
    if client == 'cenit':
        return cenit_co(cenit_co_conf, mto_df, piping_class)
