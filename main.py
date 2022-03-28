from src.mto_exist.mto_exist import mto_exist
from src.mto_does_not_exist import mto_does_not_exist
from src.summary import summary
from src.mr import mr
from src.clean_csv import clean_csv


if __name__ == '__main__':
    mto_already_exist = False

    if not mto_already_exist:
        mto_does_not_exist()
    else:
        mto_exist()

    # co()
    summary()
    mr()
    clean_csv()
