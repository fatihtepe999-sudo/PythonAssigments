from datetime import datetime


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.is_blocked = False
        self.basket = []

    def logout(self):
        print(f"Logging out user: {self.username}")


class Market:
    def __init__(self):
        # market inventory
        self.inventory = {
            'Asparagus': {'stock': 10, 'price': 5},
            'Broccoli': {'stock': 15, 'price': 6},
            'Carrots': {'stock': 18, 'price': 7},
            'Apples': {'stock': 20, 'price': 5},
            'Banana': {'stock': 10, 'price': 8},
            'Berries': {'stock': 30, 'price': 3},
            'Eggs': {'stock': 50, 'price': 2},
            'Mixed fruit juice': {'stock': 0, 'price': 8},
            'Fish Sticks': {'stock': 25, 'price': 12},
            'Ice Cream': {'stock': 32, 'price': 6},
            'Apple Juice': {'stock': 40, 'price': 7},
            'Orange Juice': {'stock': 30, 'price': 8},
            'Grape Juice': {'stock': 10, 'price': 9}
        }

    def update_inventory(self, product, amount):  # this function change amount when user bought something
        if product in self.inventory:
            self.inventory[product]['stock'] += amount

def search_product(user, market): # this function for search product in market inventory
    search_product = (input("What are you searching for? ")).lower()
    # I used .lower() because Capital letter is not important
    counter = 0  # this counter for calculate how many similar item found
    similar_items_list = []  # this list empty. I will append search results
    for product in market.inventory:  # this line make a loop in market inventory
        # if input which taking from user in product dictionary and market has stock.
        if search_product in product.lower() and market.inventory[product]['stock'] > 0 and search_product != "":
            counter += 1  # for calculate how many result we have.
            similar_items_list.append(product)  # this line fill in list with results
    while counter == 0 or search_product == "":  # if user input does not match any items.
        search_product = input("Your search did not match any items. Please try something else (Enter 0 for main menu):")
        # We will take another input from user, and we will give a chance for main menu.
        for product in market.inventory:
            if search_product.lower() in product.lower() and market.inventory[product]['stock'] > 0 and search_product != "":
                counter += 1  # for calculate how many result we have.
                similar_items_list.append(product)  # this line fill in list with results
            elif search_product == "0":  # if input is 0
                main_menu(user, market)  # user will go to main menu.

    print(f"found {counter} similar items:")
    for index in range(len(similar_items_list)):  # this line make loop.
        print(f"{index + 1}.{similar_items_list[index]} {market.inventory[similar_items_list[index]]['price']}$")
        #  {ordinal number}. {product name}                  {price}
    #  and user will choose from list
    selection = int(input("Please select which item you want to add to your basket (Enter 0 for main menu): "))
    if 1 <= selection <= len(similar_items_list):
        selected_item = similar_items_list[selection - 1]
        # if user choose 1, I need to subtract one number because ı will use index for write product
        amount = int(input(f"Adding {selected_item}.Enter the amount: "))
        add_to_basket(user, market, selected_item, amount)


def add_to_basket(user, market, selected_item, amount):
    if amount == 0:
        main_menu(user, market)
    elif amount <= market.inventory[selected_item]['stock']:  # if market inventory has stock enough
        # Add to basket
        user.basket.append({'product': selected_item, 'price': market.inventory[selected_item]['price'], 'amount': amount})
        print(f"Added {selected_item} into your Basket.")
        print("Going back to main menu...")
    else:  # if market stocks is not enough I will want to another number from user
        print("Sorry! The amount exceeds the limit. Please try again with a smaller amount.")
        add_to_basket(user, market, selected_item, int(input("Enter the amount(0 for main menu): ")))


def see_basket(user, market, repeat=0):  # this function helps to see basket
    if repeat == 1:  # this repeat value for use different place see basket function
        print("\nYour basket contains:")
    total_price = 0
    for i, item in enumerate(user.basket, 1):  # this line make loop from each item in user's basket
        product = item['product']
        price = item['price']
        amount = item['amount']
        total = price * amount  # calculate total price each of items
        total_price += total  # calculate total price
        print("{}. {} price={}{} amount={} total={}{}".format(i, product, price, '$', amount, total, '$'))

    if user.basket != []:  # if user's basket is not empty:
        print("Total {}{}".format(total_price, '$'))
        basket_menu(user, market)
    else:  # if user's basket empty
        print("Your basket is empty. Total 0$")


def basket_menu(user, market):
    print("\nPlease choose an option:")
    print("1. Update amount\n2. Remove an item\n3. Check out\n4. Go back to main menu")
    choice = input("Your selection: ")
    #  user will choose a number between 1 and 4. different things from these number code will return basket submenu
    if choice == '1':
        update_amount(user, market)
    elif choice == '2':
        remove_item(user, market)
    elif choice == '3':
        check_out(user, market)
    elif choice == '4':
        main_menu(user, market)
    else:
        print("Invalid selection. Returning to basket submenu.")
        basket_menu(user, market)


def update_amount(user, market):
    print("\nPlease select which item to change its amount:")

    for i, item in enumerate(user.basket, 1):
        product = item['product']
        price = item['price']
        amount = item['amount']
        total = price * amount
        print("{}. {} price={}{} amount={} total={}{}".format(i, product, price, '$', amount, total, '$'))
    # until here same thing with see basket function
    # but after this user choose items which he or she wants to change amount
    selection = int(input("Enter the number of the item: "))
    if 1 <= selection <= len(user.basket):  # user should choose number between 1 and length of basket
        selected_item = user.basket[selection - 1]  # There is a minus 1 because index equals to selection minus 1 .
        new_amount = int(input("Please type the new amount: "))

        if new_amount <= market.inventory[selected_item['product']]['stock']:  # if stock is enough for new amount
            selected_item['amount'] = new_amount   # I will change amount
            print("\nYour basket now contains:")
            see_basket(user, market, 1)
        else:  # if stock is not enough for change amount
            print("Sorry! The new amount exceeds the limit. Please try again with a smaller amount.")
            update_amount(user, market)
    else:  # if user does not choose valid number
        print("Invalid selection. Returning to basket submenu.")


def remove_item(user, market):  # this function for remove an item
    print("\nPlease select which item to remove:")
    for i, item in enumerate(user.basket, 1):
        product = item['product']
        price = item['price']
        amount = item['amount']
        total = price * amount
        print("{}. {} price={}$ amount={} total={}$".format(i, product, price, amount, total))
    # until here same with see_basket
    # after this it is similar change amount
    selection = int(input("Enter the number of the item: "))
    if 1 <= selection <= len(user.basket):
        removed_item = user.basket.pop(selection - 1)
        market.update_inventory(removed_item['product'], removed_item['amount'])
        print("\nYour basket now contains:")
        see_basket(user, market)
    else:
        print("Invalid selection. Returning to basket submenu.")


def check_out(user, market):
    print("\nProcessing your receipt...")
    print("******* Medipol Online Market ********")
    print("**************************************")
    print("444 8 544")
    print("medipol.edu.tr")
    print("————————————")

    total_price = 0
    for item in user.basket:
        product = item['product']
        price = item['price']
        amount = item['amount']
        total = price * amount
        total_price += total
        print("{} {}$ amount={} total={}{}".format(product, price, amount, total, '$'))
        market.update_inventory(item, -amount)  # amount sign is minus because stock will decrease

    print("————————————")
    print(f"Total {total_price}$")
    print("————————————")
    print(datetime.now().strftime("%Y/%m/%d %H:%M"))  # this is not belongs to me
    print("Thank You for using our Market!")

    user.basket = []  # Clear the user's basket after checkout
    main_menu(user, market)


def login_system():
    users = {'ahmet': {'password': '1234', 'blocked': False, 'login_attempts': 0},
             'zeynep': {'password': '4444', 'blocked': False, 'login_attempts': 0},
             'admin': {'password': 'qwerty', 'blocked': False, 'login_attempts': 0}}

    market = Market()

    while True:
        print("\n**** Welcome to Medipol Online Market ****")
        print("Please log in by providing your user credentials")
        username = input("User Name: ")
        password = input("Password: ")

        if username in users and not users[username]['blocked'] and users[username]['password'] == password:
            print("Successfully logged in!")
            if username == 'admin':  # if user is admin
                admin_menu(users, market)  # it is going to admin_menu
            else:  # if user is not admin
                user = User(username, password)  # This line create a class
                main_menu(user, market)  # and user will go to main_menu
        else:
            print("Your user name and/or password is not correct. Please try again!")

            if username in users:
                users[username]['login_attempts'] += 1  # this value increase wrong password

                if users[username]['login_attempts'] >= 3:  # if users input three wrong password
                    users[username]['blocked'] = True   # user blocked. Admin can activate from admin_menu
                    print("Your account has been blocked. Please contact the administrator.")


def main_menu(user, market):
    while True:
        print(f"\nWelcome, {user.username}! Please choose one of the following options by entering the corresponding menu number.")
        print("Please choose one of the following services:")
        print("1. Search for a product\n2. See Basket\n3. Check Out\n4. Logout\n5. Exit")
        choice = input("Your Choice: ")

        if choice == '1':
            search_product(user, market)
        elif choice == '2':
            see_basket(user, market)
        elif choice == '3':
            check_out(user, market)
        elif choice == '4':
            user.logout()
            login_system()
        elif choice == '5':
            exit()  # this function ends the code.
        else:
            print("Invalid selection. Please provide a valid menu number.")


def admin_menu(users, market):  # if user is admin this window will open
    while True:
        print("\nWelcome, Admin! Please choose one of the following options by entering the corresponding menu number.")
        print("Please choose one of the following services:")
        print("1. Activate User Account\n2. Deactivate User Account\n3. Add User\n4. Remove User\n5. Logout\n6. Exit")
        choice = input("Your Choice: ")

        if choice == '1':
            activate_user_account(users)
        elif choice == '2':
            deactivate_user_account(users)
        elif choice == '3':
            add_user(users)
        elif choice == '4':
            remove_user(users)
        elif choice == '5':
            login_system()
        elif choice == '6':
            exit()
        else:
            print("Invalid selection. Please provide a valid menu number.")


def activate_user_account(users):
    username = input("Enter the username to activate: ")
    if username in users and users[username]['blocked']:
        users[username]['blocked'] = False
        print(f"User account '{username}' has been activated.")
    else:
        print("User not found or account is not blocked. Please try again.")


def deactivate_user_account(users):
    username = input("Enter the username to deactivate: ")
    if username in users and not users[username]['blocked']:
        users[username]['blocked'] = True
        print(f"User account '{username}' has been deactivated.")
    else:
        print("User not found or account is already blocked. Please try again.")


def add_user(users):
    username = input("Enter the new username: ")
    if username not in users:
        password = input("Enter the password for {}: ".format(username))
        users[username] = {'password': password, 'blocked': False, 'login_attempts': 0}
        print(f"User '{username}' has been added.")
    else:
        print("Username already exists. Please choose another username.")


def remove_user(users):
    username = input("Enter the username to remove: ")
    if username in users:
        del users[username]
        print(f"User '{username}' has been removed.")
    else:
        print("User not found. Please try again.")

# start program
login_system()
