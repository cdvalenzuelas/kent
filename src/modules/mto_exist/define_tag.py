def define_tag(mto_df, piping_class):
    def search_tag(row):
        type_code, spec, first_size, second_size = row

        sub_df = piping_class[(piping_class['TYPE_CODE']
                               == type_code) & (piping_class['SPEC'] == spec) & (piping_class['FIRST_SIZE'] == first_size) & (piping_class['SECOND_SIZE'] == second_size)]

        if sub_df.size > 0:
            return sub_df.iloc[0]['TAG']
        else:
            return '-'

    # Busqueda de tag
    mto_df['TAG'] = mto_df[['TYPE_CODE', 'SPEC', 'FIRST_SIZE', 'SECOND_SIZE']].apply(
        search_tag, axis=1)

    return mto_df