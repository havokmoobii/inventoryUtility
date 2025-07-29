# Constants and Enums

from enum import Enum

class Categories(Enum):
    PREBUILD = (0, 'PREBUILD')
    OPENLOOP = (1, 'OPEN-LOOP')
    SERVER = (2, 'SERVER / BILL / IT')
    LAPTOP = (3, 'LAPTOP')
    NUC = (4, 'NUC')
    PRC = (5, 'PRC')
    FAN = (6, 'FAN')
    MBD = (7, 'MBD')
    MEM = (8, 'MEM')
    HDR = (9, 'HDR')
    VDO = (10, 'VDO')
    CAS = (11, 'CAS')
    POW = (12, 'POW')
    MISC = (13, 'MISC')
    MAX_CATEGORIES = (14, 'Error: MAX_CATEGORIES text should not display.')

class EntryStep(Enum):
    PROMPT = 0
    ORDER_NUMBER = 1
    CATEGORY = 2
    DATE = 3
    ITEM_LIST = 4
    NOTES = 5
    DONE = 6
    QUIT = 7

BACK_COMMAND = 'back'
QUIT_COMMAND = 'quit'
CLEAR_COMMAND = 'clear'
DATE_MIN_LENGTH = 5
CAT_CODE_LENGTH = 3
CATEGORIES_INDEX_INDEX = 0
CATEGORIES_TEXT_INDEX = 1
ORDER_LOC_CATEGORY_INDEX = 0
ORDER_LOC_INNER_INDEX = 1