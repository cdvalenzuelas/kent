from src.modules.mto_exist.mto_exist import mto_exist
from src.modules.mto_does_not_exist import mto_does_not_exist
from src.modules.summary import summary
from src.modules.mr import mr
from src.utils.clean_csv import clean_csv


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
