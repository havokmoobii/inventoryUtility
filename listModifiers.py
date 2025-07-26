# List Modifiers

# All the functions that modify the staged list and its entries.

from constants import (Categories, EntryStep, BACK_COMMAND, QUIT_COMMAND,
                       CLEAR_COMMAND, DATE_MIN_LENGTH, CAT_CODE_LENGTH,
                       CATEGORIES_INDEX_INDEX, CATEGORIES_TEXT_INDEX)


def get_order_number(staged_list, current_entry):
    order_number = input('Enter an SO number: ')

    if len(order_number) == 7 and order_number.isdecimal:
        current_entry[EntryStep.ORDER_NUMBER] = order_number
        return EntryStep.CATEGORY
    elif order_number.lower() == BACK_COMMAND or order_number.lower() == QUIT_COMMAND:
        return EntryStep.QUIT
    return EntryStep.ORDER_NUMBER

def get_category(current_entry):
    print('\nOrder Category\n')
    print(f'1. {Categories.PREBUILD.value[CATEGORIES_TEXT_INDEX]}')
    print(f'2. {Categories.OPENLOOP.value[CATEGORIES_TEXT_INDEX]}')
    print(f'3. {Categories.SERVER.value[CATEGORIES_TEXT_INDEX]}')
    print(f'4. {Categories.LAPTOP.value[CATEGORIES_TEXT_INDEX]}')
    print(f'5. {Categories.NUC.value[CATEGORIES_TEXT_INDEX]}')
    print('6. Other\n')

    category = input('Enter the category number: ')

    if category == '1':
        current_entry[EntryStep.CATEGORY] = Categories.PREBUILD
        current_entry[EntryStep.DATE] = None
        return EntryStep.ITEM_LIST
    elif category == '2':
        current_entry[EntryStep.CATEGORY] = Categories.OPENLOOP
        return EntryStep.DATE
    elif category == '3':
        current_entry[EntryStep.CATEGORY] = Categories.SERVER
        return EntryStep.DATE
    elif category == '4':
        current_entry[EntryStep.CATEGORY] = Categories.LAPTOP
        return EntryStep.DATE
    elif category == '5':
        current_entry[EntryStep.CATEGORY] = Categories.NUC
        return EntryStep.DATE
    elif category == '6':
        current_entry[EntryStep.CATEGORY] = None
        return EntryStep.DATE
    elif category.lower() == BACK_COMMAND:
        return EntryStep.ORDER_NUMBER
    elif category.lower() == QUIT_COMMAND:
        return EntryStep.QUIT
    
def get_date(current_entry):
    date = input('\nEnter the date that the order was created: ')
    
    if date.lower() == BACK_COMMAND:
        return EntryStep.CATEGORY
    elif date.lower() == QUIT_COMMAND:
        return EntryStep.QUIT
    # Honestly this step is just because I keep forgetting the date step and start entering item codes.
    elif len(date) != DATE_MIN_LENGTH:
        print("Error: Date must be in format MM/DD")
        return EntryStep.DATE
    else:
        current_entry[EntryStep.DATE] = date
        return EntryStep.ITEM_LIST
    
def get_item_list(current_entry, item_list):
    print('\nEnter the items this order is staged for one at a time.')
    print('Enter "clear" to start this step over.')
    current_item = input('Enter nothing to move on to the next step: ')

    if current_item.lower() == CLEAR_COMMAND:
        item_list = ''
        # Reset category if it is one that is determined at this step.
        if (current_entry[EntryStep.CATEGORY] != Categories.PREBUILD and
        current_entry[EntryStep.CATEGORY] != Categories.OPENLOOP and
        current_entry[EntryStep.CATEGORY] != Categories.SERVER and
        current_entry[EntryStep.CATEGORY] != Categories.LAPTOP and
        current_entry[EntryStep.CATEGORY] != Categories.NUC):
            current_entry[EntryStep.CATEGORY] = None
        current_entry[EntryStep.ITEM_LIST] = None
        return EntryStep.ITEM_LIST, item_list
    elif current_item.lower() == BACK_COMMAND:
        if current_entry[EntryStep.CATEGORY] == Categories.PREBUILD:
            return EntryStep.CATEGORY, item_list
        else:
            return EntryStep.DATE, item_list
    elif current_item.lower() == QUIT_COMMAND:
        return EntryStep.QUIT, item_list
    elif current_item == '':
        if current_entry[EntryStep.CATEGORY] == None:
            current_entry[EntryStep.CATEGORY] = Categories.MISC
        return EntryStep.NOTES, item_list
    else:
        if len(current_item) < CAT_CODE_LENGTH:
            print(f'\nError: Entry must be at least {CAT_CODE_LENGTH} characters long.')
        else:
            if item_list == '':
                item_list += current_item
                if current_entry[EntryStep.CATEGORY] == None:
                    current_entry[EntryStep.CATEGORY] = assign_category(item_list[:CAT_CODE_LENGTH])
            else: 
                item_list += f', {current_item}'    
            current_entry[EntryStep.ITEM_LIST] = item_list
            return EntryStep.ITEM_LIST, item_list
        
def get_notes(staged_list, current_entry):
    notes = input('\nEnter any additional notes about the order: ')

    if notes.lower() == BACK_COMMAND:
        return EntryStep.ITEM_LIST
    elif notes.lower() == QUIT_COMMAND:
        return EntryStep.QUIT
    else:
        if notes != "":
            current_entry[EntryStep.NOTES] = notes
        staged_list[current_entry[EntryStep.CATEGORY].value[CATEGORIES_INDEX_INDEX]].append(current_entry)
        return EntryStep.QUIT

def assign_category(first_item):
        # Apparantly you can't access individual items inside tuples that are part of an Enum in a match statement?
    match(first_item):
        case 'PRC':
            return Categories.PRC
        case 'FAN':
            return Categories.FAN
        case 'MBD':
            return Categories.MBD
        case 'MEM':
            return Categories.MEM
        case 'HDR':
            return Categories.HDR
        case 'VDO':
            return Categories.VDO
        case 'CAS':
            return Categories.CAS
        case 'POW':
            return Categories.POW
    return Categories.MISC