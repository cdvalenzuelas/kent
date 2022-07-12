def find_tag(row, piping_class):
    line, type_code, spec, size, qty = row

    # Si no hay válvulas no buscar tags
    if qty == 0:
        return None

    # Detectar las válvulas que cumplen con el type_code, spec y diámetro
    sub_piping_class = piping_class[(
        piping_class['TYPE_CODE'] == type_code) &
        (piping_class['SPEC'] == spec) &
        (piping_class['FIRST_SIZE_NUMBER'] == size)]

    # Determinar cuantas válvulas cuentan con las características anteriores
    shape = sub_piping_class.shape[0]

    # Si sólo hay una válvula que le ponga el tag correspondiente
    if shape == 1:
        return sub_piping_class.loc[:, 'TAG'].tolist()[0]
    # Si no se encuentra la válvula mostrar un error, puede ser que el archivo de P&ID esté mal
    elif shape == 0:
        print(
            f'❌ NO SE ENCUENTRAN VÁLVULAS CON SPECS {spec}, TYPE_CODE {type_code} y DIÁMETRO {size} EN LA LÍNEA {line}, REVISAR EL ARCHIVO p&id.csv\n')
        return 'error'
    # Si hay más de un tipo de válvula para estas combinaciones de SPEC, TYPE_CODE y DIÁMETRO se le pide al usuario que confirme
    else:
        # Se resetea el índice
        sub_piping_class.reset_index(inplace=True)

        # Se le dice al usuario que hay más de una posibilidad y que debe elejir
        print(f"""----------------------------------------------------------------------------------------------------------------------------------------------------
HAY MÁS DE UN TIPO DE VÁLVULA QUE CUMPLE CON LOS REQUISITOS DE SPECS {spec} EN LA LÍNEA {line}, TYPE_CODE {type_code} y DIÁMETRO {size}, 
LAS OPCIONES CORRECTAS SON:\n""")

        # Se le muestran las opciones al usuario
        print(sub_piping_class[['TAG', 'DESCRIPTION']])

        # El usuario elije la opción correcta
        index = int(input('\nSELECCIONES EL NUMERAL CORRECTO: '))

        # La herramienta extrae el tag correcto
        tag = sub_piping_class.loc[index, 'TAG']

        # Se le agrega el tag faltate al archivo p&id.csv
        return tag


def search_valve_tag(pid_df, piping_class):
    # Hacer una copia del piping class
    piping_class = piping_class.copy()
    pid_df = pid_df.copy()

    pid_df['TAG'] = pid_df[['LINE_NUM', 'TYPE_CODE', 'SPEC', 'FIRST_SIZE_NUMBER', 'QTY']].apply(
        find_tag, axis=1, piping_class=piping_class)

    print('----------------------------------------------------------------------------------------------------------------------------------------------------\n')

    return pid_df
