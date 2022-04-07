from src.modules.mto_exist.mto_diagnostic import define_diganostic
from src.modules.mto_exist.mto_cleaner import mto_cleaner


def mto_exist():
    # Generar un MTO limpio
    mto_df = mto_cleaner()

    # Hacer diagnóstico del MTO entregado
    mto_df = define_diganostic(mto_df)

    # Convertir datos
    mto_df.convert_dtypes().dtypes

    # Crear registro de items sin identificar
    mto_df_na = mto_df[mto_df['SHORT_DESCRIPTION'].isnull()]

    mto_df_na = mto_df_na[['LINE_NUM', 'QTY', 'common_index']]

    mto_df_na.to_csv('./output/mto_temp.csv', index=True)

    # Eliminar columnas innecesarias
    mto_df.drop(['common_index'], axis=1, inplace=True)

    # Crear el archivo de MTO
    mto_df.to_csv('./output/mto.csv', index=True)
