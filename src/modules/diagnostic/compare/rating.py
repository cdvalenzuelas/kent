import re
from src.utils.normalize_string import normalize_string


def def_rating(mto_diagnostic, short_desc_2, short_description_2, rating, type_code):
    rating_in_bom = False
    rating_in_piping_class = False
    rating_diacnostic = ''

    mto_diagnostic = '' if mto_diagnostic == None else mto_diagnostic

    if rating != '-' and type_code != 'BOLT':
        sub_str = normalize_string(rating)

        print(sub_str)

        # Verificar si el ratingedule existe en el bom y en el piping class
        rating_in_bom = sub_str in short_desc_2
        rating_in_piping_class = sub_str in short_description_2

        # Ver diferencias entre el bom y el rating y el piping class y el rating
        rating_diacnostic = rating_diacnostic + \
            f'EL RATING DEL ELEMENTO NO SE ENCUENTRA EN EL B.O.M, ESTE DEBERÍA SER {rating}.\n' if not rating_in_bom else rating_diacnostic

        rating_diacnostic = rating_diacnostic + \
            f'EL RATING DEL ELEMENTO NO SE ENCUENTRA EN EL PINPING CLASS, ESTE DEBERÍA SER {rating}.\n' if not rating_in_piping_class else rating_diacnostic

        # Si hay diferencias retornar el diagnóistico
        if rating_diacnostic != '':
            return mto_diagnostic + rating_diacnostic
        else:
            return mto_diagnostic

    else:
        return mto_diagnostic
