def second_diacnostic(mto_diagnostic_2, item, line_num, type_code, first_size, second_size, short_description):
    # Escribir en el archivo de cosas importantes
    if mto_diagnostic_2 != '':
        mto_diagnostic_2 = f'ITEM {item}: {line_num} , {type_code}, {first_size}{second_size}\n---------------------------------------\n{mto_diagnostic_2}\n'

    if str(short_description) != 'nan':
        with open('./output/diagnostic_descriptions_and_weights.txt', mode='a') as f:
            f.write(mto_diagnostic_2)
