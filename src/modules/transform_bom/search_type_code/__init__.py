from src.modules.transform_bom.search_type_code.define_type_code import define_type_code


# (VALEC17) BUSCAR EL TYPE_CODE DE CADA UNO DE LOS ELEMENTOS
def search_type_code(bom_df, cad_software):
    # (VALEC17) HACER LA COPIA BOM
    bom_df = bom_df.copy()

    if cad_software == 'autoplant':
        bom_df['STYPE'] = bom_df['COMPONENT DESCRIPTION'].apply(
            define_type_code)

    if cad_software == 'cadworks':
        bom_df['DB_CODE'] = bom_df['SHORT_DESC'].apply(define_type_code)

    if cad_software == 'smartplant':
        bom_df['TYPE CODE (VER HOJA ABREVIATURAS)'] = bom_df['DESCRIPCIÓN'].apply(
            define_type_code)

    return bom_df
