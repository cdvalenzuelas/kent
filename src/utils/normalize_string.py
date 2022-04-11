def normalize_string(string):
    string = str(string).upper().replace('"', '').replace('.', '').replace(
        ',', '').replace(';', '').replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U').replace('-', '').replace(' ', '')

    return string
