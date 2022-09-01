import re


def def_sch(mto_diagnostic, short_desc_2, short_description_2, type_code, sch, diagnostic_dict):
    sch_in_bom = False
    sch_in_piping_class = False
    sch_diacnostic = ''
    real_sch = ''

    mto_diagnostic = '' if mto_diagnostic == None else mto_diagnostic

    # Si el elemento de tubería tiene sch en el piping class
    if sch != '-':
        schs = re.sub(' ', '', sch).split('x')

        # (VALEC17) Contruir el string sch que no son reductores
        if len(schs) == 1:
            sub_str = f'SCH{schs[0]}'
            real_sch = schs[0]

        # (VALEC17) Contruir el string sch de los reductores
        else:
            # (VALEC17) Los weldolets se tratan de manera distinta
            if type_code == 'WOL':
                sub_str = f'SCH{schs[1]}'
                real_sch = schs[1]
            else:
                sub_str = f'SCH{schs[0]}X{schs[1]}'
                real_sch = sch

        # (VALEC17) Verificar si el schedule existe en el bom y en el piping class
        sch_in_bom = sub_str in short_desc_2
        sch_in_piping_class = sub_str in short_description_2

        # (VALEC17) Ver diferencias entre el bom y el sch y el piping class y el sch
        sch_diacnostic = sch_diacnostic + \
            f'EL SCH DEL ELEMENTO NO SE ENCUENTRA EN EL B.O.M, ESTE DEBERÍA SER {real_sch}.\n' if not sch_in_bom else sch_diacnostic

        sch_diacnostic = sch_diacnostic + \
            f'EL SCH DEL ELEMENTO NO SE ENCUENTRA EN EL PINPING CLASS, ESTE DEBERÍA SER {real_sch}.\n' if not sch_in_piping_class else sch_diacnostic

        # (VALEC17) Si hay diferencias retornar el diagnóistico
        if sch_diacnostic != '':
            diagnostic_dict['sch_piping'].append(real_sch)

            return (mto_diagnostic + sch_diacnostic, diagnostic_dict)
        else:
            diagnostic_dict['sch_piping'].append(None)

            return (mto_diagnostic, diagnostic_dict)

    else:
        diagnostic_dict['sch_piping'].append(None)

        return (mto_diagnostic, diagnostic_dict)
