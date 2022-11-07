from src.modules.transform_bom.search_type_code.valves import valves
from src.modules.transform_bom.search_type_code.strainers import strainers
from src.modules.transform_bom.search_type_code.misscelaneous import misscelaneous
from src.modules.transform_bom.search_type_code.flanges import flanges
from src.modules.transform_bom.search_type_code.pipes import pipes
from src.modules.transform_bom.search_type_code.olets import olets


# (VALEC17) DEFINIR EL TYPE CODE
def define_type_code(description):
    # (VALEC17) PASAR A MAYUSCULA
    description = description.upper()

    # (VALEC17) EL TYPE CODE
    type_code = '-'

    # (VALEC17) BUSCAR EL TYPE_CODE DEPENDIENDO DEL TIPO DE ELEMENTO
    if description != '-' or str(description) != 'nan':
        # (VALEC17) VER SI SON FIGURAS EN 8
        if 'FIGURE-8' in description or 'SPECTACLE BLANK' in description:
            return 'F8'
        # (VALEC17) VER SI TIENE  VÁLVULAS
        elif 'VALVE' in description:
            type_code = valves(description)
        # (VALEC17) VER SI TIENE STRAINERS
        elif 'STRAINER' in description:
            type_code = strainers(description)
        # (VALEC17) VER SI TIENE NIPLES
        elif 'NIPPLE' in description:
            type_code = 'NIP'
        # (VALEC17) VER SI TIENE TUBERÍAS
        elif 'PIPE' in description:
            type_code = pipes(description)
        # (VALEC17) VER SI TIENE BRIDAS
        elif 'FLANGE' in description:
            type_code = flanges(description)
        # (VALEC17) VER SI TIENE KITS DE AISLAMIENTO
        elif 'KIT' in description and 'ISOLATING' in description:
            type_code = 'KIT'
        # (VALEC17) VER SI TIENE STUD BOLTS
        elif 'STUD BOLT' in description:
            type_code = 'BOLT'
        # (VALEC17) VER SI TIENE KITS GASKETS NORMALES
        elif 'GASKET' in description:
            type_code = 'GAS'
        # (VALEC17) VER SI TIENE KITS OLTES
        elif 'OLET' in description:
            type_code = olets(description)
        # (VALEC17) VER SI TIENE CODOS DE 45
        elif 'ELBOW' in description and '45' in description:
            type_code = '45L'
        # (VALEC17) VER SI TIENE CODOS DE 90
        elif 'ELBOW' in description and '90' in description:
            type_code = '90L'
        # (VALEC17) VER SI TIENE COUPLINGS
        elif 'COUPLING' in description:
            type_code = 'CPL'
        # (VALEC17) VER SI TIENE CAPS
        elif 'CAP' in description:
            type_code = 'CAP'
        # (VALEC17) VER SI TIENE TEES REDUCTORAS
        elif 'REDUCING TEE' in description:
            type_code = 'RTE'
        # (VALEC17) VER SI TIENE TEES
        elif 'TEE' in description:
            type_code = 'TEE'
        # (VALEC17) VER SI TIENE REDUCCIONES CONCÉNTRICAS
        elif 'CONCENTRIC REDUCER' in description:
            type_code = 'CRE'
        # (VALEC17) VER SI TIENE REDUCCIONES ECCÉNTRICAS
        elif 'ECCENTRIC REDUCER' in description:
            type_code = 'ERE'
        # (VALEC17) VER SI TIENE SWAGES CONCENTRICOS
        elif 'CONCENTRIC SWAGE' in description:
            type_code = 'SWC'
        # (VALEC17) VER SI TIENE UNIONES UNIVERSALES
        elif 'UNION' in description:
            type_code = 'UNN'
        # (VALEC17) VER SI TIENE UNIONES UNIVERSALES
        elif 'PLUG' in description:
            type_code = 'PLG'
        # (VALEC17) EN CASO DE QUE NO SE ENCUENTRE NADA MIRAR EN MISCELANEOS
        else:
            type_code = misscelaneous(description)

    return type_code
