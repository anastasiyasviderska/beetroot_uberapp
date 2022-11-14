from basic_user import BasicUser
import json


class Driver(BasicUser):

    def draw_menu(self):
        with open('database.json', 'r') as pnm:
            data = json.load(pnm)
            rating = data[self.username]['rating']

        menu = f"\n{'-' * 40}\n\nHello Driver {self.username}, rating {rating}\n1. Sign Out\n2. Available Orders" \
               f"\n3. See income\n4. Executed Orders\n5. Change password\n6. Open Help Desk\n7. Exit\n"
        try:
            selected_menu = int(input(menu))
            match selected_menu:
                case 1:
                    return self.uber_server.sign_out(self.username)
                case 2:
                    filter_max_value = 0
                    filter_min_value = 0
                    filter_type_value = None
                    available_orders = self.uber_server.get_available_orders()
                    while True:
                        is_empty_list = True
                        print(f"\n{'-' * 40}\n\nB. Back to Driver menu\nP. Filter by total price\nD. Filter by distance\nR. Filter by price per kilometer\n{'-' * 40}")
                        available_ids = ['b', 'p', 'd', 'r']
                        for order in available_orders:
                            match filter_type_value:
                                case 'Price':
                                    if order['price'] > filter_min_value and order['price'] < filter_max_value:
                                        is_empty_list = False
                                        available_ids.append(str(order['id']))
                                        print(f"{order['id']}. from: {order['start_location']} to: {order['destination']}"
                                            f" price: {order['price']} status: {order['order_status']}")
                                case 'Distance':
                                    if order['distance'] > filter_min_value and order['distance'] < filter_max_value:
                                        is_empty_list = False
                                        available_ids.append(str(order['id']))
                                        print(f"{order['id']}. from: {order['start_location']} to: {order['destination']}"
                                            f" price: {order['price']} status: {order['order_status']}")
                                case 'Rate':
                                    rate = order['price'] / order ['distance']
                                    if rate > filter_min_value and rate < filter_max_value:
                                        is_empty_list = False
                                        available_ids.append(str(order['id']))
                                        print(f"{order['id']}. from: {order['start_location']} to: {order['destination']}"
                                            f" price: {order['price']} status: {order['order_status']}, rate: {rate:9.2f} $/km")
                                case _:
                                    available_ids.append(str(order['id']))
                                    is_empty_list = len(available_ids) == 0
                                    print(f"{order['id']}. from: {order['start_location']} to: {order['destination']}"
                                        f" price: {order['price']} status: {order['order_status']}")
                        if is_empty_list:
                            print("💥 Nothing was found")
                        selected_id = input("Please choose an action or an order to execute (use index): ")
                        while selected_id not in available_ids:
                            selected_id = input("Please choose a valid action or order to execute (use index): ")
                        match selected_id:
                            case 'B':
                                break
                            case 'P':
                                filter_min_value = int(input("Please enter minimum total price: "))
                                filter_max_value = int(input("Please enter maximum total price: "))
                                filter_type_value = "Price"
                            case 'D':
                                filter_min_value = int(input("Please enter minimum distance: "))
                                filter_max_value = int(input("Please enter maximum distance: "))
                                filter_type_value = "Distance"
                            case 'R':
                                filter_min_value = int(input("Please enter minimum rate per km: "))
                                filter_max_value = int(input("Please enter maximum rate per km: "))
                                filter_type_value = "Rate"
                            case _:
                                selected_id = int(selected_id)
                                self.raise_income_in_orders(selected_id)
                                self.update_money_in_db()
                                self.uber_server.execute_order(selected_id, self.username)
                                break
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
                    self.change_password()
                case 6:
                    self.open_help_desk()
                case 7:
                    self.uber_server.sign_out(self.username)
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

