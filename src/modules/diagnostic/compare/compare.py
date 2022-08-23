from src.utils.normalize_string import normalize_string
from src.modules.diagnostic.compare.description import description
from src.modules.diagnostic.compare.weight import weight
from src.modules.diagnostic.compare.bolts_length import bolt_length as def_bolt_length
from src.modules.diagnostic.compare.nipple_option import nipple_option
from src.modules.diagnostic.compare.wafer_bolts import wafer_bolts
from src.modules.diagnostic.compare.sch import def_sch
from src.modules.diagnostic.compare.rating import def_rating

# (VALEC17) Escribir el diagnóstico
from src.modules.diagnostic.write.main_diacnostic import main_diacnostic
from src.modules.diagnostic.write.second_diacnostic import second_diacnostic


def compare(row):
    item, line_num, type_code, short_desc, short_description, weight_x, weight_y, length, bolt_length, qty, bolt_weight, first_size, bolt_diameter, second_size, rating, shc = row

    # (VALEC17) Cambiar las descripciones
    short_desc_2 = normalize_string(short_desc)
    short_description_2 = normalize_string(short_description)

    # (VALEC17) Cambiar el second_size
    second_size = f'{int(bolt_length)}mm ({first_size}, # (VALEC17){rating})' if type_code == 'BOLT' else second_size
    second_size = '' if second_size == '-' else f'x{second_size}'

    # (VALEC17) Cambiar el first_size
    first_size = bolt_diameter if type_code == 'BOLT' else first_size

    # (VALEC17) Empezar a crear el diagnóstico
    diagnostic = ''
    diagnostic_2 = ''

    # (VALEC17) Ver diferencias en descripciones
    diagnostic_2 = description(diagnostic_2, short_desc_2,
                               short_description_2, short_desc)

    # (VALEC17) diferencias en pesos
    diagnostic_2 = weight(diagnostic_2, type_code,
                          weight_x, weight_y, bolt_weight, qty, length)

    # (VALEC17) bolts length
    diagnostic = def_bolt_length(diagnostic, type_code, length, bolt_length)

    # (VALEC17) nipple option
    diagnostic = nipple_option(diagnostic, type_code, length)

    # (VALEC17) wafer_bolts
    diagnostic = wafer_bolts(diagnostic, type_code)

    # (VALEC17) Comparar sch
    diagnostic = def_sch(diagnostic, short_desc_2,
                         short_description_2, type_code, shc)

    # (VALEC17) Comparar el rating
    diagnostic = def_rating(diagnostic, short_desc_2,
                            short_description_2, rating, type_code)

    # (VALEC17) Main diagnostic
    main_diacnostic(diagnostic, short_description, item,
                    line_num, type_code, first_size, second_size)

    # (VALEC17) Second diagnostic
    second_diacnostic(diagnostic_2, item, line_num,
                      type_code, first_size, second_size, short_description)

    return item
