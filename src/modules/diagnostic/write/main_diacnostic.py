def main_diacnostic(mto_diagnostic, short_description, item, line_num, type_code, first_size, second_size):
    # Escribir en el archivo de cosas importantes
    if mto_diagnostic != '':
        mto_diagnostic = f'ITEM {item}: {line_num} , {type_code}, {first_size}{second_size}\n---------------------------------------\n{mto_diagnostic}\n'

    if str(short_description) != 'nan':
        with open('./output/diagnostic.txt', mode='a') as f:
            f.write(mto_diagnostic)
