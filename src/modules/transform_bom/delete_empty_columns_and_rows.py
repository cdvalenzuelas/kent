import pandas as pd


def delete_empty_columns_and_rows():
    bom_df = pd.read_csv('./inputs/bom.csv')

    # Recoger las columnas que no se encuetran nombradas
    unnamed_columns = [
        column for column in bom_df.columns if column.startswith('Unnamed')]

    # Eliminar las columnas que no se encuetran nombradas
    bom_df.drop(unnamed_columns, inplace=True, axis=1)

    # Lenar campos vacíos
    bom_df.fillna('-', inplace=True)

    # Definir si las filas son vacías o no

    def def_na(row, columns):
        cond = True

        for column in columns:
            if row[column] != '-':
                cond = False
                break

        return cond

    # Definir si las filas son vacías o no
    bom_df['NA'] = bom_df.apply(def_na, axis=1, columns=bom_df.columns)

    # Eliminar las filas vacías
    bom_df = bom_df[(bom_df['NA'] == False)]

    # Eliminar las columnas innecesarias
    bom_df.drop(['NA'], axis=1, inplace=True)

    # Retornar el bom_df sin columnas ni filas cacías
    return bom_df
