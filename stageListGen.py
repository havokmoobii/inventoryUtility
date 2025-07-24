# Staged List Generator

# A tool to help me build my biweekly email.

# Staged list will build a list of lists of dictionaries.

from enum import Enum

class Categories(Enum):
    PREBUILD = 'PREBUILD'
    OPENLOOP = 'OPEN-LOOP'
    SERVER = 'SERVER / BILL / IT'
    LAPTOP = 'LAPTOP'
    NUC = 'NUC'
    PRC = 'PRC'
    FAN = 'FAN'
    MBD = 'MBD'
    MEM = 'MEM'
    HDR = 'HDR'
    VDO = 'VDO'
    CAS = 'CAS'
    POW = 'POW'
    MISC = 'MISC'

class EntryStep(Enum):
    ORDER_NUMBER = 0
    CATEGORY = 1
    DATE = 2
    ITEM_LIST = 3
    NOTES = 4

def stageListGen():
    staged_list = []

    for category in Categories:
        staged_list.append([category.value])

    while True:

        print('')
        print(staged_list)

        print('\nStaged List Generator\n')
        print('1. Entry Mode')
        print('2. Edit Mode')
        print('3. Exit')

        selection = input('\nEnter the number of your selection: ')

        if selection == '1':
            entryMode(staged_list)
        if selection == '2':
            pass
        if selection == '3':
            return

def entryMode(staged_list):
    entry_step = EntryStep.ORDER_NUMBER
    current_entry = {EntryStep.CATEGORY: None}

    while True:
        if current_entry != {EntryStep.CATEGORY: None}:
            print(f'\n{current_entry}')

        match(entry_step):
            case EntryStep.ORDER_NUMBER:
                print('')
                print(staged_list)
                print('\nEntry Mode\n')
                print('Follow the prompts to add entries to the staged list.')
                print('"back" can be entered at any time to go back to the previous question')
                print('"quit" can be entered at any time to return to the previous menu\n')

                order_number = input('Enter an SO number: ')

                if len(order_number) == 7 and order_number.isdecimal:
                    current_entry[EntryStep.ORDER_NUMBER] = order_number
                    entry_step = EntryStep.CATEGORY
                elif order_number.lower() == 'back' or order_number.lower() == 'quit':
                    return
                continue

            case EntryStep.CATEGORY:
                print('\nOrder Category\n')
                print(f'1. {Categories.PREBUILD.value}')
                print(f'2. {Categories.OPENLOOP.value}')
                print(f'3. {Categories.SERVER.value}')
                print(f'4. {Categories.LAPTOP.value}')
                print(f'5. {Categories.NUC.value}')
                print('6. Other\n')

                category = input('Enter the category number: ')

                if category == '1':
                    current_entry[EntryStep.CATEGORY] = Categories.PREBUILD
                    current_entry[EntryStep.DATE] = None
                    entry_step = EntryStep.ITEM_LIST
                elif category == '2':
                    current_entry[EntryStep.CATEGORY] = Categories.OPENLOOP
                    entry_step = EntryStep.DATE
                elif category == '3':
                    current_entry[EntryStep.CATEGORY] = Categories.SERVER
                    entry_step = EntryStep.DATE
                elif category == '4':
                    current_entry[EntryStep.CATEGORY] = Categories.LAPTOP
                    entry_step = EntryStep.DATE
                elif category == '5':
                    current_entry[EntryStep.CATEGORY] = Categories.NUC
                    entry_step = EntryStep.DATE
                elif category == '6':
                    current_entry[EntryStep.CATEGORY] = None
                    entry_step = EntryStep.DATE
                elif category.lower() == 'back':
                    entry_step = EntryStep.ORDER_NUMBER
                elif category.lower() == 'quit':
                    return
                continue

            case EntryStep.DATE:
                # I could be strict with the format on this, but this tool is for my own use.
                # So I wont.
                date = input('Enter the date that the order was created: ')