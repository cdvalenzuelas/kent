import pandas as pd


# (VALEC17) Extraer el piping class
def cenit_piping_class():
    CS1SC2 = pd.read_csv('./src/clients/cenit/piping_class/CS1SC2.csv')
    CS2SA1 = pd.read_csv('./src/clients/cenit/piping_class/CS2SA1.csv')
    CS3SA1 = pd.read_csv('./src/clients/cenit/piping_class/CS3SA1.csv')
    CS4SA1 = pd.read_csv('./src/clients/cenit/piping_class/CS4SA1.csv')
    CS5SA1 = pd.read_csv('./src/clients/cenit/piping_class/CS5SA1.csv')
    CS6SA1 = pd.read_csv('./src/clients/cenit/piping_class/CS6SA1.csv')
    CS2SD2 = pd.read_csv('./src/clients/cenit/piping_class/CS2SD2.csv')

    piping_class = pd.concat(
        [CS1SC2, CS2SA1, CS3SA1, CS4SA1, CS5SA1, CS6SA1, CS2SD2])

    piping_class.fillna('-', inplace=True)

    return piping_class
