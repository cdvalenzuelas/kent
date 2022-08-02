import pandas as pd

from src.utils.normalize_string import normalize_string
from src.modules.diagnostic.compare.description import description
from src.modules.diagnostic.compare.weight import weight
from src.modules.diagnostic.compare.bolts_length import bolt_length as def_bolt_length
from src.modules.diagnostic.compare.nipple_option import nipple_option
from src.modules.diagnostic.compare.wafer_bolts import wafer_bolts
from src.modules.diagnostic.compare.sch import def_sch
from src.modules.diagnostic.compare.rating import def_rating

# Escribir el diagnóstico
from src.modules.diagnostic.write.main_diacnostic import main_diacnostic
from src.modules.diagnostic.write.second_diacnostic import second_diacnostic


def compare(row, diagnostic_dict):
    item, line_num, type_code, short_desc, short_description, weight_x, weight_y, length, bolt_length, qty, bolt_weight, first_size, bolt_diameter, second_size, rating, shc, tag = row

    # Cambiar las descripciones
    short_desc_2 = normalize_string(short_desc)
    short_description_2 = normalize_string(short_description)

    # Cambiar el second_size
    second_size = f'{int(bolt_length)}mm ({first_size}, #{rating})' if type_code == 'BOLT' else second_size
    second_size = '' if second_size == '-' else f'x{second_size}'

    # Cambiar el first_size
    first_size = bolt_diameter if type_code == 'BOLT' else first_size

    # Empezar a crear el diagnóstico
    diagnostic = ''
    diagnostic_2 = ''

    # Crear indice
    diagnostic_dict['index'].append('-')

    # Ver diferencias en descripciones
    diagnostic_2, diagnostic_dict = description(diagnostic_2, short_desc_2,
                                                short_description_2, short_desc, diagnostic_dict)

    # diferencias en pesos
    diagnostic_2, diagnostic_dict = weight(diagnostic_2, type_code,
                                           weight_x, weight_y, bolt_weight, qty, length, diagnostic_dict)

    # bolts length
    diagnostic, diagnostic_dict = def_bolt_length(
        diagnostic, type_code, length, bolt_length, diagnostic_dict)

    # nipple option
    diagnostic = nipple_option(diagnostic, type_code, length)

    # wafer_bolts
    diagnostic = wafer_bolts(diagnostic, type_code)

    # Comparar sch
    diagnostic, diagnostic_dict = def_sch(diagnostic, short_desc_2,
                                          short_description_2, type_code, shc, diagnostic_dict)

    # Comparar el rating
    diagnostic, diagnostic_dict = def_rating(diagnostic, short_desc_2,
                                             short_description_2, rating, type_code, diagnostic_dict)

    # print(diagnostic_dict)
    print(pd.DataFrame(diagnostic_dict))

    # Main diagnostic
    main_diacnostic(diagnostic, short_description, item,
                    line_num, type_code, first_size, second_size)

    # Second diagnostic
    second_diacnostic(diagnostic_2, item, line_num,
                      type_code, first_size, second_size, short_description)

    return item
