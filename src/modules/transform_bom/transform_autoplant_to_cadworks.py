import pandas as pd


def transform_autoplant_to_cadworks(bom_df):
    # (VALEC17) Hacer una copia del df
    bom_df = bom_df.copy()

    # (VALEC17) Agregando columnas adicionaels
    bom_df['SHORT_DESC'] = bom_df['COMPONENT DESCRIPTION']
    bom_df['TAG'] = '-'
    bom_df['THK_NOM'] = '-'

    # (VALEC17) Diccionario de longitudes, pesos, tamaños principales y tamaños secundarios
    new_fields_dict = {
        'WEIGHT': [],
        'LENGTH': [],
        'MAIN_NOM': [],
        'RED_NOM': [],
        'QTY': []
    }

    # (VALEC17) Definir longitudes, pesos, tamaños principales y tamaños secundarios
    for index, row in bom_df.iterrows():
        # (VALEC17) Definir pesos
        if row['PESO'] == '-':
            new_fields_dict['WEIGHT'].append(0)
        else:
            new_fields_dict['WEIGHT'].append(row['PESO'])

        # (VALEC17) Definir longitudes
        # (VALEC17) Definir longitud de tuberías
        if row['STYPE'] in ['PE', 'BE', 'TE']:
            # (VALEC17) Dejar únicamente la parte numérica
            length = row['QUANTITY'].replace(' m', '')
            # (VALEC17) Dejar la longitud en milímetros
            length = float(length)*1000
            if length > 0:
                new_fields_dict['LENGTH'].append(length)
            else:
                new_fields_dict['LENGTH'].append(1)
        # (VALEC17) Definir la longitud de niples
        elif row['STYPE'] == 'NIP':
            new_fields_dict['LENGTH'].append(0)
        # (VALEC17) Longitud de pernos
        elif row['STYPE'] == 'BOLT':
            # (VALEC17) Extaer la longitud de los pernos
            length = row['SIZE'].upper().replace(
                ' ', '').split('X')[1].replace('M', '')
            new_fields_dict['LENGTH'].append(float(length)*1000)
        else:
            # (VALEC17) Si no pertenece a tuberías, niples y bolts se asume la longitud como 0
            new_fields_dict['LENGTH'].append(0)

        # (VALEC17) Definir los diámetros principales
        sizes = row['SIZE'].upper().replace(' ', '').split('X')
        sizes_len = len(sizes)

        if row['STYPE'] == 'NIP':
            new_fields_dict['MAIN_NOM'].append(f'{sizes[0]}"')
            new_fields_dict['RED_NOM'].append('-')
        elif row['STYPE'] not in ['BOLT']:
            if sizes_len == 1:
                new_fields_dict['MAIN_NOM'].append(f'{sizes[0]}"')
                new_fields_dict['RED_NOM'].append('-')
            elif sizes_len == 2:
                new_fields_dict['MAIN_NOM'].append(f'{sizes[0]}"')
                # (VALEC17) Si es un sockoled o un weldolet
                second_size = sizes[1].split('ON')
                new_fields_dict['RED_NOM'].append(f'{second_size[0]}"')
        else:
            new_fields_dict['MAIN_NOM'].append('0"')
            new_fields_dict['RED_NOM'].append('-')

        # (VALEC17) Definir las cantidades
        if row['STYPE'] in ['PE', 'BE', 'TE']:
            new_fields_dict['QTY'].append(1)
        else:
            new_fields_dict['QTY'].append(row['QUANTITY'])

    # (VALEC17) Concatenar el bom con el nuevo df
    new_fields_df = pd.DataFrame(new_fields_dict)

    bom_df.reset_index(drop=True, inplace=True)

    bom_df = pd.concat([bom_df, new_fields_df], axis=1)

    # (VALEC17) Renombrar columnas
    bom_df.rename(columns={
        'ITEM': 'MARK',
        'LINE NUMBER': 'LINE_NUM',
        'SPEC': 'SPEC_FILE',
        'STYPE': 'DB_CODE',
        'COMPONENT DESCRIPTION': 'DESCRIPTION'
    }, inplace=True)

    # (VALEC17) Eliminar las columnas innecesarias
    bom_df.drop(['GTYPE', 'SCHEDULE', 'RATING', 'FACING',
                'UNITS', 'PESO', 'QUANTITY'], axis=1, inplace=True)

    # (VALEC17) Reorganizar columnas
    bom_df = bom_df[['MARK', 'LINE_NUM', 'SPEC_FILE', 'DB_CODE', 'DESCRIPTION', 'SHORT_DESC',
                    'SIZE', 'MAIN_NOM', 'RED_NOM', 'THK_NOM', 'QTY', 'TAG', 'LENGTH', 'WEIGHT']]

    return bom_df
