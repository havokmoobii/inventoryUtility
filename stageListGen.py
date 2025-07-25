# Staged List Generator

# A tool to help me build my biweekly email.

# Staged list will build a list of lists of dictionaries.

from enum import Enum

class Categories(Enum):
    PREBUILD = {0: 'PREBUILD'}
    OPENLOOP = {1: 'OPEN-LOOP'}
    SERVER = {2: 'SERVER / BILL / IT'}
    LAPTOP = {3: 'LAPTOP'}
    NUC = {4: 'NUC'}
    PRC = {5: 'PRC'}
    FAN = {6: 'FAN'}
    MBD = {7: 'MBD'}
    MEM = {8: 'MEM'}
    HDR = {9: 'HDR'}
    VDO = {10: 'VDO'}
    CAS = {11: 'CAS'}
    POW = {12: 'POW'}
    MISC = {13: 'MISC'}
    MAX_CATEGORIES = {14: 'Error: MAX_CATEGORIES text should not display'}

class EntryStep(Enum):
    ORDER_NUMBER = 0
    CATEGORY = 1
    DATE = 2
    ITEM_LIST = 3
    NOTES = 4

BACK_COMMAND = 'back'
QUIT_COMMAND = 'quit'
CLEAR_COMMAND = 'clear'

def stageListGen():
    staged_list = []

    # To Do: Make a function to print this out exactly how the final email will be formatted.
    for category in Categories:
        if category != Categories.MAX_CATEGORIES:
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
    item_list = ''

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
                elif order_number.lower() == BACK_COMMAND or order_number.lower() == QUIT_COMMAND:
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
                elif category.lower() == BACK_COMMAND:
                    entry_step = EntryStep.ORDER_NUMBER
                elif category.lower() == QUIT_COMMAND:
                    return
                continue

            case EntryStep.DATE:
                # I could be strict with the format on this, but this tool is for my own use.
                # So I wont.
                date = input('Enter the date that the order was created: ')
                
                if date.lower() == BACK_COMMAND:
                    entry_step = EntryStep.CATEGORY
                elif date.lower() == QUIT_COMMAND:
                    return
                else:
                    current_entry[EntryStep.DATE] = date
                continue

            case EntryStep.ITEM_LIST:
                print('Enter the items this order is staged for one at a time.')
                print('Enter "clear" to start this step over.')
                current_item = input('Enter nothing to move on to the next step: ')

                if current_item.lower() == CLEAR_COMMAND:
                    item_list = ''
                elif current_item.lower() == BACK_COMMAND:
                    entry_step = EntryStep.DATE
                    item_list = ''
                elif current_item.lower() == QUIT_COMMAND:
                    return
                elif current_item == '':
                    current_entry[EntryStep.ITEM_LIST] = item_list
                    entry_step = EntryStep.NOTES
                else:
                    if item_list == '':
                        item_list += current_item
                    else: 
                        item_list += f', {current_item}'
                continue

            case EntryStep.NOTES:
                notes = input('Enter any additional notes about the order: ')

                if current_item.lower() == BACK_COMMAND:
                    entry_step = EntryStep.DATE
                elif current_item.lower() == QUIT_COMMAND:
                    return
                else:
                    current_entry[EntryStep.NOTES] = notes
                    staged_list[current_entry[EntryStep.CATEGORY]].append(current_entry)
                    return
                continue

def assign_category(first_item):
    pass