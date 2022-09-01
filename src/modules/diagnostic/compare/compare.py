import pandas as pd

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

# Verificar si los elementos de tubería no tienen diferencias con piping class


def def_difference(row):
    description_spec, description_piping, weight_spec, weight_piping, bolt_length_spec, bolt_length_piping, sch_piping, rating_piping = row

    cond_1 = description_spec == '-'
    cond_2 = description_piping == '-'
    cond_3 = weight_spec == '-'
    cond_4 = weight_piping == '-'
    cond_5 = bolt_length_spec == '-'
    cond_6 = bolt_length_piping == '-'
    cond_7 = sch_piping == '-'
    cond_8 = rating_piping == '-'

    return cond_1 and cond_2 and cond_3 and cond_4 and cond_5 and cond_6 and cond_7 and cond_8


def compare(row, diagnostic_dict):
    spec, item, line_num, type_code, short_desc, short_description, weight_x, weight_y, length, bolt_length, qty, bolt_weight, first_size, bolt_diameter, second_size, rating, shc, tag = row

    # (VALEC17) Cambiar las descripciones
    short_desc_2 = normalize_string(short_desc)
    short_description_2 = normalize_string(short_description)

    # (VALEC17) Cambiar el second_size
    second_size = f'{int(bolt_length)}mm ({first_size}, # {rating})' if type_code == 'BOLT' else second_size
    second_size = '' if second_size == '-' else f'x{second_size}'

    # (VALEC17) Cambiar el first_size
    first_size = bolt_diameter if type_code == 'BOLT' else first_size

    # (VALEC17) Empezar a crear el diagnóstico
    diagnostic = ''
    diagnostic_2 = ''

    # (VALEC17) Crear indice
    diagnostic_dict['index'].append(
        f'{spec} {type_code} {first_size} {second_size} {tag}')

    # (VALEC17) Ver diferencias en descripciones
    diagnostic_2, diagnostic_dict = description(diagnostic_2, short_desc_2,
                                                short_description_2, short_desc, short_description, diagnostic_dict)

    # (VALEC17) diferencias en pesos
    diagnostic_2, diagnostic_dict = weight(diagnostic_2, type_code,
                                           weight_x, weight_y, bolt_weight, qty, length, diagnostic_dict)

    # (VALEC17) bolts length
    diagnostic, diagnostic_dict = def_bolt_length(
        diagnostic, type_code, length, bolt_length, diagnostic_dict)

    # (VALEC17) nipple option
    diagnostic = nipple_option(diagnostic, type_code, length)

    # (VALEC17) wafer_bolts
    diagnostic = wafer_bolts(diagnostic, type_code)

    # (VALEC17) Comparar sch
    diagnostic, diagnostic_dict = def_sch(diagnostic, short_desc_2,
                                          short_description_2, type_code, shc, diagnostic_dict)

    # (VALEC17) Comparar el rating
    diagnostic, diagnostic_dict = def_rating(diagnostic, short_desc_2,
                                             short_description_2, rating, type_code, diagnostic_dict)

    # (VALEC17) print(diagnostic_dict)
    diagnostic_df = pd.DataFrame(diagnostic_dict)
    diagnostic_df.fillna('-', inplace=True)

    diagnostic_df.drop_duplicates(['index'], inplace=True)

    # Eliminar los elementos que no presentan problemas en descripciones, ratings, pesos, longitudes etc
    diagnostic_df['difference'] = diagnostic_df[[
        'description_spec', 'description_piping', 'weight_spec', 'weight_piping', 'bolt_length_spec', 'bolt_length_piping', 'sch_piping', 'rating_piping']].apply(def_difference, axis=1)

    diagnostic_df = diagnostic_df[(diagnostic_df['difference'] == False)]

    diagnostic_df.to_csv('diagnostic.csv')

    ''' diagnostic_dict = {
        'index': [],
        'description_spec': [],
        'description_piping': [],
        'weight_spec': [],
        'weight_piping': [],
        'bolt_length_spec': [],
        'bolt_length_piping': [],
        'sch_piping': [],
        'rating_piping': []
    } '''

    ''' print(
        diagnostic_dict['index'][len(diagnostic_dict['index']) - 1],
        len(diagnostic_dict['index']),
        len(diagnostic_dict['description_spec']),
        len(diagnostic_dict['description_piping']),
        len(diagnostic_dict['weight_spec']),
        len(diagnostic_dict['weight_piping']),
        len(diagnostic_dict['bolt_length_spec']),
        len(diagnostic_dict['bolt_length_piping']),
        len(diagnostic_dict['sch_piping']),
        len(diagnostic_dict['rating_piping']),
        'ERROR' if len({len(diagnostic_dict['index']),
                        len(diagnostic_dict['description_spec']),
                        len(diagnostic_dict['description_piping']),
                        len(diagnostic_dict['weight_spec']),
                        len(diagnostic_dict['weight_piping']),
                        len(diagnostic_dict['bolt_length_spec']),
                        len(diagnostic_dict['bolt_length_piping']),
                        len(diagnostic_dict['sch_piping']),
                        len(diagnostic_dict['rating_piping'])}) > 1 else ''
    ) '''

    # (VALEC17) Main diagnostic
    main_diacnostic(diagnostic, short_description, item,
                    line_num, type_code, first_size, second_size)

    # (VALEC17) Second diagnostic
    second_diacnostic(diagnostic_2, item, line_num,
                      type_code, first_size, second_size, short_description)

    return item
