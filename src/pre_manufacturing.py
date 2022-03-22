def pre_manufacturing(row):
    description, item_class, sch, first_size, second_size = row

    second_size = f'x{second_size}' if second_size != '-' else ''
    sch = f', S-{sch}' if sch != '-' else ''
    item_class = f', #{item_class}' if item_class != '-' else ''

    return f'PREFABRICACIÓN DE {description}, {first_size}{second_size}{sch}{item_class}'
