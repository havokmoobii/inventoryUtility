# Staged List Generator

# A tool to help me build my biweekly email.

# Staged list will build a list of lists of dictionaries.

# Next Time: Work on Edit Mode. It can reuse a lot of the entry mode code. Probably
# have it list all the entrys, have the user choose to edit or delete a selected entry,
# and make it current_entry if they select edit and work through the entry step process from there.
# Idea: Make the list save itself to a file regularly, so progress cannot be lost.

from constants import Categories, EntryStep, CATEGORIES_TEXT_INDEX
from listModifiers import get_order_number, get_category, get_date, get_item_list, get_notes

def stagedListGen():
    staged_list = []

    # To Do: Make a function to print this out exactly how the final email will be formatted.
    for category in Categories:
        if category != Categories.MAX_CATEGORIES:
            staged_list.append([category.value])

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
            pass
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
                entry_step = get_notes(staged_list, current_entry)
                continue
            case EntryStep.QUIT:
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
            print("")