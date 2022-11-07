from basic_user import BasicUser
import json


class Driver(BasicUser):

    def draw_menu(self):
        menu = f"\n{'-' * 40}\n\nHello Driver {self.username}\n1. Sign Out\n2. Available Orders\n3. Income\n" \
               f"4. Executed Orders\n5. Exit\n"
        try:
            selected_menu = int(input(menu))
            match selected_menu:
                case 1:
                    return self.uber_server.sign_out()
                case 2:
                    available_orders = self.uber_server.get_available_orders()
                    print(f"\n{'-' * 40}\n\n0. Back to Driver menu")
                    for order in available_orders:
                        print(f"id: {order['id']}. from: {order['start_location']} to: {order['destination']}"
                              f" price: {order['price']} status: {order['order_status']}")
                    selected_id = int(input("Please choose order to execute(use id): "))
                    match selected_id:
                        case 0:
                            pass
                        case _:
                            self.raise_income_in_orders(selected_id)
                            self.update_money_in_db()
                            self.uber_server.execute_order(selected_id, self.username)
                    return None
                case 3:
                    print(f"Your income is: {self.amount_of_money}")
                case 4:
                    executed_orders = self.uber_server.get_executed_orders(self.username)
                    print(f"\n{'-' * 40}\n")
                    for order in executed_orders:
                        print(f"id: {order['id']}. from: {order['start_location']} to: {order['destination']}"
                              f" price: {order['price']} status: {order['order_status']}")
                    return None
                case 5:
                    exit()
        except ValueError:
            return None

    def raise_income_in_orders(self, id):
        with open('database_orders.json', 'r') as database_orders_file:
            data = json.load(database_orders_file)
            for order_dict in data:
                if order_dict['id'] == id:
                    if order_dict["order_status"] == "created":
                        self.amount_of_money += int(order_dict['price'])
                    else:
                        print("This order is already executed!")

