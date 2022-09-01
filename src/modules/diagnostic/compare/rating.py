import re
from src.utils.normalize_string import normalize_string


def def_rating(mto_diagnostic, short_desc_2, short_description_2, rating, type_code, diagnostic_dict):
    rating_in_bom = False
    rating_in_piping_class = False
    rating_diacnostic = ''

    mto_diagnostic = '' if mto_diagnostic == None else mto_diagnostic

    if rating != '-' and type_code != 'BOLT':
        sub_str = normalize_string(rating)

        # (VALEC17) Verificar si el ratingedule existe en el bom y en el piping class
        rating_in_bom = sub_str in short_desc_2
        rating_in_piping_class = sub_str in short_description_2

        # (VALEC17) Ver diferencias entre el bom y el rating y el piping class y el rating
        rating_diacnostic = rating_diacnostic + \
            f'EL RATING DEL ELEMENTO NO SE ENCUENTRA EN EL B.O.M, ESTE DEBERÍA SER {rating}.\n' if not rating_in_bom else rating_diacnostic

        rating_diacnostic = rating_diacnostic + \
            f'EL RATING DEL ELEMENTO NO SE ENCUENTRA EN EL PINPING CLASS, ESTE DEBERÍA SER {rating}.\n' if not rating_in_piping_class else rating_diacnostic

        # (VALEC17) Si hay diferencias retornar el diagnóistico
        if rating_diacnostic != '':
            diagnostic_dict['rating_piping'].append(rating)

            return (mto_diagnostic + rating_diacnostic, diagnostic_dict)
        else:
            diagnostic_dict['rating_piping'].append(None)

            return (mto_diagnostic, diagnostic_dict)

    else:
        diagnostic_dict['rating_piping'].append(None)

        return (mto_diagnostic, diagnostic_dict)
