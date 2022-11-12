from basic_user import BasicUser
import json


class Passenger(BasicUser):
    def draw_menu(self):
        menu = f"\n{'-'*40}\n\nHello Passenger {self.username}\n1. Sign Out\n2. Place an Order\n3. " \
               f"List of Orders\n4. Rate a driver\n5. Add money\n6. See balance\n7. Change password" \
               f"\n8. Open Help Desk\n9. Exit\n"
        try:
            selected_menu = int(input(menu))
            match selected_menu:
                case 1:
                    return self.uber_server.sign_out(self.username)
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
                        print(f"id: {order['id']}, from: {order['start_location']} to: {order['destination']} price: {order['price']} status: {order['order_status']}")
                    return None
                case 4:
                    executed_orders = self.uber_server.get_executed_orders(self.username)
                    print(f"\n{'-' * 40}\n")
                    print("List of your unrated uber rides:")
                    set_of_orders = set()
                    for order in executed_orders:
                        if order["is_rated"] == "rated":
                            continue
                        set_of_orders.add(str(order["id"]))
                        print(f"id: {order['id']} from {order['start_location']} to: {order['destination']}"
                              f" price: {order['price']} driver's name: {order['driver_username']}")

                    if len(set_of_orders) != 0:
                        print("id: 0. Go back")
                        order_to_rate = input("Please choose the id of the ride that you want to rate or go back: ")
                        while order_to_rate not in set_of_orders:
                            if order_to_rate == '0':
                                break
                            print("You typed a wrong id!")
                            order_to_rate = input("Please choose the id of the ride that you want to rate or go back: ")
                        if order_to_rate != '0':
                            self.rate_a_driver(order_to_rate)
                    else:
                        print("You don't have any orders unrated!")
                    return None
                case 5:
                    self.add_money_to_balance()
                    self.update_money_in_db()
                case 6:
                    print(f"Your balance is {self.amount_of_money}")
                case 7:
                    self.change_password()
                case 8:
                    self.open_help_desk()
                case 9:
                    self.uber_server.sign_out(self.username)
                    exit()

        except ValueError:
            return None

    def add_money_to_balance(self):
        how_much_money = int(input("Please choose the amount of money you want to add in your account: "))
        if how_much_money > 0:
            self.amount_of_money += how_much_money
            print(f"Your new balance is {self.amount_of_money}")
        else:
            print("Your added money can't be smaller than zero!")

    def pay_order(self, order_price):
        self.amount_of_money -= order_price

    @staticmethod
    def rate_a_driver(index_of_order):
        number_of_stars = 0
        while not 1 <= number_of_stars <= 5:
            number_of_stars = int(input("Please rate the chosen ride with a number from 1 to 5: "))

        driver_username = None
        with open("database_orders.json", 'r+') as orders_db:
            orders_dict = json.load(orders_db)
            for order in orders_dict:
                if order["id"] == int(index_of_order):
                    order["is_rated"] = "rated"
                    driver_username = order["driver_username"]

            orders_db.seek(0)
            json.dump(orders_dict, orders_db, indent=4)
            orders_db.truncate()

        with open("database.json", 'r+') as drivers_db:
            data = json.load(drivers_db)
            # print(data[driver_username])
            data[driver_username]['number_of_ratings'] += 1
            number_of_ratings = data[driver_username]['number_of_ratings']
            rating_sum = float(data[driver_username]['rating']) * (number_of_ratings - 1) + number_of_stars
            data[driver_username]['rating'] = f"{rating_sum / number_of_ratings:.2f}"

            drivers_db.seek(0)
            json.dump(data, drivers_db, indent=4)
            drivers_db.truncate()

