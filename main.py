# Inventory Utility

# Tools to make my day job as an Inventory Supervisor easier

# Tool 1: Map Formatter: Takes a list of order numbers produced from voice
# texting and formats it into an easy to read list to be made into a map.

# Tool 2: Staged List Email Generator: A tool that takes order information
# and missing parts and sorts it into a list for my biweekly emails.

from mapFormatter import mapFormatter
from stageListGen import stageListGen

def main():

    while True:
        print('\nInventory Utility\n')
        print('1. Map Formatter')
        print('2. Staged List Email Generator - NYI')
        print('3. Exit')
        selection = input('\nEnter the number of your selection: ')
        
        if selection == '1':
            mapFormatter()
        if selection == '2':
            stageListGen()
        if selection == '3':
            return

if __name__ == '__main__':
    main()
