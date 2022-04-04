# Se deben buscar los datos que relacionan las cantidades de obra
def define_co(mto_df, piping_class):

    def search_co(row):
        type_code, spec, rating = row

        sub_df = None

        if type_code != 'BOLT':
            sub_df = piping_class[(piping_class['TYPE_CODE']
                                   == type_code) & (piping_class['SPEC'] == spec) & (piping_class['RATING'] == rating)]
        else:
            sub_df = piping_class[(piping_class['TYPE_CODE']
                                   == type_code) & (piping_class['SPEC'] == spec)]

        if sub_df.size > 0:
            return sub_df.iloc[0]['CO']
        else:
            return '-'

    # Establecer el suministro de las cantidades de obra
    # mto_df['CO'] = mto_df[['TYPE_CODE', 'SPEC', 'RATING']].apply(
        # search_co, axis=1)

    return mto_df
