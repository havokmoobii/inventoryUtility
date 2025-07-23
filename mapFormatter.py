# Map Formatter

# Takes a list of order numbers produced from voice texting and
# formats it into an easy to read list to be made into a map.

# Context: I use voice texting to make a list of staged orders
# and thier location. Voice texting makes a mess of said list.
# This is a tool to clean it up.

def mapFormatter():
    input('\nPaste an unformatted list of orders into formatterInput.txt and press enter to continue: ')
    print("")

    with open('formatterInput.txt', 'r') as f:
          raw_map = f.read()

    # Voice texting includes dashes and spaces somewhat randomly. They need to be removed.
    order_list_with_dashes = raw_map.split()

    order_list = []
    for item in order_list_with_dashes:
        if '-' in item:
            order_list.extend(item.split('-'))
        else:
            order_list.append(item)

    # Voice texting will remove the first digit of an order number if it is the same as the
    # preceding rack number, so I decided it was easier to omit the rack numbers when using
    # voice texting and add them in the formatting process.
    rack_num = 1
    order_map = ""

    for item in order_list:
        if item == 'rack':
            order_map += f"Rack {rack_num}\n"
            rack_num += 1
        else:
            order_map += f"{item}\n"

    order_map.strip('\n')
    print(order_map)

    # I sometimes remove orders from the list after this stage, so I don't want to directly
    # convert it to a pdf yet.
    print("Formatting Complete. Copy the above list into Word")

    input('Press enter to return to the menu: ')