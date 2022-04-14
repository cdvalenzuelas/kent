# Reemplaza puntos por comas
def replace_dot_by_comma(data):
    if type(data) == float or type(data) == int:
        if data % 1 == 0:
            data = str(int(data))
        else:
            data = str(data)

    data = data.replace('.', ',')

    return data
