from basic_user import BasicUser
import json


class Passenger(BasicUser):
    def draw_menu(self):
        menu = f"\n{'-'*40}\n\nHello Passenger {self.username}\n1. Sign Out\n2. Place an Order\n3. " \
               f"List of Orders\n4. Add money\n5. See balance\n6. Exit\n"
        try:
            selected_menu = int(input(menu))
            match selected_menu:
                case 1:
                    return self.uber_server.sign_out()
                case 2:
                    start_location = input('Please enter your start location: ')
                    destination = input('Please enter your destination: ')
                    price = int(input("Please enter your price: "))
                    if self.amount_of_money > price > 0:
                        self.uber_server.create_new_order(self.username, start_location, destination, price)
                        self.pay_order(price)
                        self.update_money_in_db()
                        print("New order created!")
                    elif price < 0:
                        print("Your price can't be smaller than zero!")
                    else:
                        print(f"You don't have enough money to place your order!"
                              f"Your balance is {self.amount_of_money}.")
                    return None
                case 3:
                    user_orders = self.uber_server.get_user_orders(self.username)
                    for order in user_orders:
                        print(f"from: {order['start_location']} to: {order['destination']} price: {order['price']} status: {order['order_status']}")
                    return None
                case 4:
                    self.add_money_to_balance()
                    self.update_money_in_db()
                case 5:
                    print(f"Your balance is {self.amount_of_money}")
                case 6:
                    exit()

        except ValueError:
            return self

    def add_money_to_balance(self):
        how_much_money = int(input("Please choose the amount of money you want to add in your account."))
        if how_much_money > 0:
            self.amount_of_money += how_much_money
            print(f"Your new balance is {self.amount_of_money}")
        else:
            print("Your added money can't be smaller than zero!")

    def pay_order(self, order_price):
        self.amount_of_money -= order_price




