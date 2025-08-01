# Staged List Generator

# A tool to help me build my biweekly email.

# Staged list will build a list of lists of dictionaries.

from constants import (Categories, EntryStep, CATEGORIES_TEXT_INDEX, CATEGORIES_INDEX_INDEX, 
                       ORDER_LOC_CATEGORY_INDEX, ORDER_LOC_INNER_INDEX, QUIT_COMMAND,
                       CAT_CODE_LENGTH)
from listModifiers import (get_order_number, get_category, get_date, get_item_list, get_notes,
                           in_list, get_order_location, assign_category)

def stagedListGen():
    staged_list = read_list_file()

    while True:
        print('\n')
        print_list(staged_list)
        print('\nStaged List Generator\n')
        print('1. Entry Mode')
        print('2. Edit Mode')
        print('3. Exit')

        selection = input('\nEnter the number of your selection: ')

        if selection == '1':
            entryMode(staged_list)
        if selection == '2':
            editMode(staged_list)
        if selection == '3':
            return

def entryMode(staged_list):
    entry_step = EntryStep.PROMPT
    current_entry = {EntryStep.ORDER_NUMBER: None,
                     EntryStep.CATEGORY: None,
                     EntryStep.DATE: None,
                     EntryStep.ITEM_LIST: None,
                     EntryStep.NOTES: None,
                     }
    item_list = ''

    while True:
        if current_entry[EntryStep.ORDER_NUMBER] != None:
            print(f'\nCurrent Entry: {get_entry_text(current_entry)}')

        match(entry_step):
            case EntryStep.PROMPT:
                print('\nEntry Mode\n')
                print('Follow the prompts to add entries to the staged list.')
                print('"back" can be entered at any time to go back to the previous question')
                print('"quit" can be entered at any time to return to the previous menu\n')
                entry_step = EntryStep.ORDER_NUMBER
                continue
            case EntryStep.ORDER_NUMBER:
                entry_step = get_order_number(staged_list, current_entry)
                continue
            case EntryStep.CATEGORY:
                entry_step = get_category(current_entry)
                continue
            case EntryStep.DATE:
                entry_step = get_date(current_entry)
                continue
            case EntryStep.ITEM_LIST:
                entry_step, item_list = get_item_list(current_entry, item_list)
                continue
            case EntryStep.NOTES:
                entry_step = get_notes(current_entry)
                continue
            case EntryStep.DONE:
                staged_list[current_entry[EntryStep.CATEGORY].value[CATEGORIES_INDEX_INDEX]].append(current_entry)
                write_list_file(staged_list)
                return
            case EntryStep.QUIT:
                return
            
def editMode(staged_list):
    while True:
        current_entry = None
        order_location = None

        print('\n')
        print_list(staged_list)
        order_number = input('\nEnter the order number to edit or "quit" to exit: ')
        if order_number.lower() == QUIT_COMMAND:
            return
        if len(order_number) == 7 and order_number.isdecimal:
            if in_list(staged_list, order_number):
                order_location = get_order_location(staged_list, order_number)
                current_entry = staged_list[order_location[ORDER_LOC_CATEGORY_INDEX]][order_location[ORDER_LOC_INNER_INDEX]]

                while(True):
                    print(f'\n{get_entry_text(current_entry)}\n')
                    print('1. Edit Entry')
                    print('2. Delete Entry')
                    print('3. Exit')

                    selection = input('\nEnter the number of your selection: ')

                    if selection == '1':
                        current_entry = staged_list[order_location[ORDER_LOC_CATEGORY_INDEX]].pop(order_location[ORDER_LOC_INNER_INDEX])
                        edit_entry(staged_list, current_entry)
                        break
                    if selection == '2':
                        staged_list[order_location[ORDER_LOC_CATEGORY_INDEX]].pop(order_location[ORDER_LOC_INNER_INDEX])
                        break
                    if selection == '3':
                        break
                write_list_file(staged_list)
            else:
                print('\nError: Order is not listed.')
        else:
            print('\nError: Invalid Order Number.')

def edit_entry(staged_list, current_entry):
    entry_step = EntryStep.PROMPT
    item_list = current_entry[EntryStep.ITEM_LIST]

    while True:
        print(f'\nCurrent Entry: {get_entry_text(current_entry)}')

        match(entry_step):
            case EntryStep.PROMPT:
                print('\nEdit Mode\n')
                print('1. Order Number')
                print('2. Category')
                print('3. Date')
                print('4. Item List')
                print('5. Notes')
                print('6. Save and Quit')

                selection = input('\nEnter the number of your selection: ')

                match(selection):
                    case '1':
                        entry_step = EntryStep.ORDER_NUMBER
                        continue
                    case '2':
                        entry_step = EntryStep.CATEGORY
                        continue
                    case '3':
                        entry_step = EntryStep.DATE
                        continue
                    case '4':
                        entry_step = EntryStep.ITEM_LIST
                        continue
                    case '5':
                        entry_step = EntryStep.NOTES
                        continue
                    case '6':
                        entry_step= EntryStep.DONE
                        continue
                    case _:
                        print('/nError: Invalid Selection!')
                        continue
                continue
            case EntryStep.ORDER_NUMBER:
                entry_step = get_order_number(staged_list, current_entry)
                if entry_step == EntryStep.CATEGORY:
                    entry_step = EntryStep.PROMPT
                continue
            case EntryStep.CATEGORY:
                entry_step = get_category(current_entry)
                if entry_step == EntryStep.DATE:
                    entry_step = EntryStep.PROMPT

                if current_entry[EntryStep.CATEGORY] == None:
                    if len(item_list) >= CAT_CODE_LENGTH:
                        current_entry[EntryStep.CATEGORY] = assign_category(item_list[:CAT_CODE_LENGTH])
                    else:
                        current_entry[EntryStep.CATEGORY] = Categories.MISC
                continue
            case EntryStep.DATE:
                if current_entry[EntryStep.CATEGORY] == Categories.PREBUILD:
                    print("\nError: Prebuild date should be None.")
                    entry_step = EntryStep.PROMPT
                else:
                    entry_step = get_date(current_entry)
                    if entry_step == EntryStep.ITEM_LIST:
                        entry_step = EntryStep.PROMPT
                continue
            case EntryStep.ITEM_LIST:
                entry_step, item_list = get_item_list(current_entry, item_list)
                if entry_step == EntryStep.NOTES:
                    entry_step = EntryStep.PROMPT
                continue
            case EntryStep.NOTES:
                entry_step = get_notes(current_entry)
                if entry_step == EntryStep.DONE:
                    entry_step = EntryStep.PROMPT
                continue
            case EntryStep.DONE:
                staged_list[current_entry[EntryStep.CATEGORY].value[CATEGORIES_INDEX_INDEX]].append(current_entry)
                return
            case EntryStep.QUIT:
                staged_list[current_entry[EntryStep.CATEGORY].value[CATEGORIES_INDEX_INDEX]].append(current_entry)
                return

def get_entry_text(current_entry):
    output = ""
    if current_entry[EntryStep.ORDER_NUMBER] != None:
        output += f'{current_entry[EntryStep.ORDER_NUMBER]}'
    if current_entry[EntryStep.DATE] != None:
        output += f' - {current_entry[EntryStep.DATE]}'
    if current_entry[EntryStep.ITEM_LIST] != None:
        output += f' - {current_entry[EntryStep.ITEM_LIST]}'
    if current_entry[EntryStep.NOTES] != None:
        output += f' - {current_entry[EntryStep.NOTES]}'
    if output == "":
        raise Exception('Error: get_entry_text should not be called with an dict full of Nones')
    return output
    
def print_list(staged_list):
    for category in staged_list:
        print(f'{category[0][CATEGORIES_TEXT_INDEX]}\n')
        if len(category) > 1:
            for i in range(1, len(category)):
                print(get_entry_text(category[i]))
            print('')

def write_list_file(staged_list):
    with open('staged_list.txt', 'w') as f:
        for category in staged_list:
            if len(category) > 1:
                for i in range(1, len(category)):
                    f.write(f'<{category[i][EntryStep.ORDER_NUMBER]}>')
                    f.write(f'<{category[i][EntryStep.CATEGORY]}>')
                    f.write(f'<{category[i][EntryStep.DATE]}>')
                    f.write(f'<{category[i][EntryStep.ITEM_LIST]}>')
                    f.write(f'<{category[i][EntryStep.NOTES]}>')
                    f.write('\n')

def read_list_file():
    staged_list = []
    raw_list = ''

    for category in Categories:
        if category != Categories.MAX_CATEGORIES:
            staged_list.append([category.value])
    try:
        with open('staged_list.txt', 'r') as f:
            raw_list = f.read()
    except:
        print('\nstaged_list.txt either does not exist or cannot be read. Creating new list.')
        return staged_list

    orders = raw_list.split('\n')
    
    for order in orders:
        if len(order) > 0:
            current_entry = {EntryStep.ORDER_NUMBER: None,
                        EntryStep.CATEGORY: None,
                        EntryStep.DATE: None,
                        EntryStep.ITEM_LIST: None,
                        EntryStep.NOTES: None,
                        }
            order_parts = order.strip('<').strip('>').split('><')
            current_entry[EntryStep.ORDER_NUMBER] = order_parts[0]
            match(order_parts[1]):
                case('Categories.PREBUILD'):
                    current_entry[EntryStep.CATEGORY] = Categories.PREBUILD
                case('Categories.OPENLOOP'):
                    current_entry[EntryStep.CATEGORY] = Categories.OPENLOOP
                case('Categories.SERVER'):
                    current_entry[EntryStep.CATEGORY] = Categories.SERVER
                case('Categories.LAPTOP'):
                    current_entry[EntryStep.CATEGORY] = Categories.LAPTOP
                case('Categories.NUC'):
                    current_entry[EntryStep.CATEGORY] = Categories.NUC
                case('Categories.PRC'):
                    current_entry[EntryStep.CATEGORY] = Categories.PRC
                case('Categories.FAN'):
                    current_entry[EntryStep.CATEGORY] = Categories.FAN
                case('Categories.MBD'):
                    current_entry[EntryStep.CATEGORY] = Categories.MBD
                case('Categories.MEM'):
                    current_entry[EntryStep.CATEGORY] = Categories.MEM
                case('Categories.HDR'):
                    current_entry[EntryStep.CATEGORY] = Categories.HDR
                case('Categories.VDO'):
                    current_entry[EntryStep.CATEGORY] = Categories.VDO
                case('Categories.CAS'):
                    current_entry[EntryStep.CATEGORY] = Categories.CAS
                case('Categories.POW'):
                    current_entry[EntryStep.CATEGORY] = Categories.POW
                case('Categories.MISC'):
                    current_entry[EntryStep.CATEGORY] = Categories.MISC
                case _:
                    raise Exception('\nError: Invalid Category\n')
            if order_parts[2] != 'None':
                current_entry[EntryStep.DATE] = order_parts[2]
            if order_parts[3] != 'None':
                current_entry[EntryStep.ITEM_LIST] = order_parts[3]
            if order_parts[4] != 'None':
                current_entry[EntryStep.NOTES] = order_parts[4]
            staged_list[current_entry[EntryStep.CATEGORY].value[CATEGORIES_INDEX_INDEX]].append(current_entry)

    return staged_list