def line_diferences(mto_df, pid_df):
    # Comparar si las lineas del P&ID se encuentrabn en el BOM
    pid_lines = set(pid_df['LINE_NUM'].unique())

    bom_lines = set(mto_df['LINE_NUM'].unique())

    pid_lines_unique = pid_lines - bom_lines
    bom_lines_unique = bom_lines - pid_lines

    # Ver la cantidad de líneas diferentes entre B.O.M y P&ID
    pid_lines_unique_size = len(pid_lines_unique)
    bom_lines_unique_size = len(bom_lines_unique)

    if pid_lines_unique_size > 0 or bom_lines_unique_size > 0:
        print(
            '❌  HAY DIFERENCIAS ENTRE LAS LÍNEAS REPORTADAS POR EL B.O.M Y EL P&ID\n')

        # Escribir en el archivo las línes que existen en un archivo y en el otro no
        with open('./output/diagnostic_p&id.txt', mode='a') as f:
            if pid_lines_unique_size > 0:

                pid_lines_unique_diacnostic = f"""
Existen {pid_lines_unique_size} líneas en el P&ID que no existe en el B.O.M y por tanto en la maqueta.
Revisar el P&ID con el objetivo de que todas las líneas nuevas estén incluidas en la maqueta.
Estas líneas son: {pid_lines_unique}. Es posible que estas líneas estén mal nombradas en la 
maqueta o que estas líneas no se encuentren ruteadas.
                """

                f.write(pid_lines_unique_diacnostic)

            if bom_lines_unique_size > 0:

                bom_lines_unique_diacnostic = f"""
Existen {bom_lines_unique_size} líneas en el B.O.M que no existe en el P&ID.
Es probable que estén símplemente mal nombradas y sea necesario rectificar.
Estas líneas son: {bom_lines_unique}. Es posible que estas líneas estén mal nombradas en la maqueta.
                """

                f.write(bom_lines_unique_diacnostic)
    else:
        print(
            '✅  NO HAY DIFERENCIAS ENTRE LAS LÍNEAS REPORTADAS POR EL B.O.M Y EL P&ID\n')

    return (bom_lines_unique, pid_lines_unique)
