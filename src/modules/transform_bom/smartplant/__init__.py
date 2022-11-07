from src.modules.transform_bom.smartplant.def_lenght import def_lenght
from src.modules.transform_bom.smartplant.def_qty import def_qty
from src.modules.transform_bom.smartplant.def_main_size import def_main_size
from src.modules.transform_bom.smartplant.def_second_size import def_second_size
from src.modules.transform_bom.smartplant.def_bolted_conection import def_bolted_conection


def smartplant(bom_df, piping_class):
    # (VALEC17) Hacer una copia del df
    bom_df = bom_df.copy()

    # (VALEC17) Agregando columnas adicionaels
    bom_df['MARK'] = bom_df['ITEM']
    bom_df['LINE_NUM'] = bom_df['NUMERO DE LÍNEA']
    bom_df['SPEC_FILE'] = bom_df['SPEC']
    bom_df['DB_CODE'] = bom_df['TYPE CODE (VER HOJA ABREVIATURAS)']
    bom_df['DESCRIPTION'] = bom_df['DESCRIPCIÓN']
    bom_df['SHORT_DESC'] = bom_df['DESCRIPCIÓN']
    bom_df['SIZE'] = '-'
    bom_df['MAIN_NOM'] = bom_df['DIAMETRO PRINCIPAL']
    bom_df['RED_NOM'] = bom_df['DIAMETRO DE BIFURCACIÓN / DIÁMETRO REDUCCIÓN / LONGITUD DE PERNOS / LONGITUD DE NIPLES']
    bom_df['THK_NOM'] = '-'
    bom_df['QTY'] = bom_df['CANTIDAD TOTAL']
    bom_df['TAG'] = '-'
    bom_df['LENGTH'] = 0
    bom_df['WEIGHT'] = bom_df['PESO TOTAL']

    # (VALEC17) RELLENAR LOS PESOS INEXISTENTES CON CERO
    bom_df['WEIGHT'].fillna(0, inplace=True)
    bom_df['WEIGHT'] = bom_df['WEIGHT'].str.replace('-', '0')

    # (VALEC17) Eliminar columnas
    bom_df.drop(columns=['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2', 'ITEM', 'NUMERO DE LÍNEA', 'SPEC', 'TYPE CODE (VER HOJA ABREVIATURAS)', 'DESCRIPCIÓN', 'DIAMETRO PRINCIPAL', 'DIAMETRO DE BIFURCACIÓN / DIÁMETRO REDUCCIÓN / LONGITUD DE PERNOS / LONGITUD DE NIPLES', 'CANTIDAD TOTAL', 'PESO TOTAL', 'RATING', 'FACE', 'TYPE (VER HOJA ABREVIATURAS)', 'AREA', 'SCHEDULE', 'UNIDAD',
                         'PESO UNITARIO'], inplace=True)

    # (VALEC17) Reorganizar columnas
    bom_df = bom_df[['MARK', 'LINE_NUM', 'SPEC_FILE', 'DB_CODE', 'DESCRIPTION', 'SHORT_DESC',
                    'SIZE', 'MAIN_NOM', 'RED_NOM', 'THK_NOM', 'QTY', 'TAG', 'LENGTH', 'WEIGHT']]

    # (VALEC17) DEFINIR LA LONGITUD DE LOS ELEMENTOS
    bom_df['LENGTH'] = bom_df[['DB_CODE', 'QTY', 'MAIN_NOM',
                               'RED_NOM', 'SHORT_DESC']].apply(def_lenght, axis=1)

    # (VALEC17) DEFINIR LAS CANTIDADES DE LOS ELEMENTOS
    bom_df['QTY'] = bom_df[['DB_CODE', 'QTY']].apply(def_qty, axis=1)

    # (VALEC17) DEFINIR EL TAMAÑO PRINCIPAL
    bom_df['MAIN_NOM'] = bom_df[['DB_CODE', 'MAIN_NOM']].apply(
        def_main_size, axis=1)

    # (VALEC17) DEFINIR EL TAMAÑO SECUNDARIO
    bom_df['RED_NOM'] = bom_df[['DB_CODE', 'RED_NOM']].apply(
        def_second_size, axis=1)

    # (VALEC17) UNA COPIA DEL BOM_DF PARA NO TENER EN CUANTA TUBERÚSA ENTERRADAS NI PREFABRICADAS
    bom_df_2 = bom_df.copy()

    # (VALEC17) NORMALIZAR LOS NOMBRES DE LÍNEA DEL BOM_DF Y LA DEL PERNO
    bom_df_2['LINE_NUM'] = bom_df_2['LINE_NUM'].str.replace(
        ' ', '').replace('(U)', '').replace('(P)', '')

    # (VALEC17) DEFINIR LOS POSIBLES DIÁMETROS DE LA CONEXIÓN PARA LOS PERNOS
    bom_df['MAIN_NOM'] = bom_df[['LINE_NUM', 'DB_CODE', 'MAIN_NOM', 'SPEC_FILE', 'TAG']].apply(
        def_bolted_conection, piping_class=piping_class, bom_df=bom_df_2, axis=1)

    return bom_df
