import pandas as pd


def supply_items(row):
    description, item_class, sch, first_size, second_size = row

    second_size = f'x{second_size}' if second_size != '-' else ''
    sch = f', S-{sch}' if sch != '-' else ''
    item_class = f', #{item_class}' if item_class != '-' else ''

    return f'SUMINISTRO DE {description}, {first_size}{second_size}{sch}{item_class}'


def supply():
    # Extraer el piping class
    CS2SA1 = pd.read_csv('./CENIT/PIPING_CLASS/CS2SA1.csv')
    CS3SA1 = pd.read_csv('./CENIT/PIPING_CLASS/CS3SA1.csv')
    CS5SA1 = pd.read_csv('./CENIT/PIPING_CLASS/CS5SA1.csv')

    CS2SA1['SUPPLY'] = CS2SA1[['DESCRIPTION', 'CLASS',
                               'SCH', 'FIRST_SIZE', 'SECOND_SIZE']].apply(supply_items, axis=1)


if __name__ == '__main__':
    pass
