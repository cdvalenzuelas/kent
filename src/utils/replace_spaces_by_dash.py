import re


def replace_spaces_by_dash(size):
    return re.sub('[\s]', '-', str(size))
