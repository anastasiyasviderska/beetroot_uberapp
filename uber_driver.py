from basic_user import BasicUser


class Driver(BasicUser):
    def draw_menu(self):
        menu = f"\n{'-'*40}\n\nHello Driver {self.username}\n1. Sign Out\n2. Available Orders\n3. Income\n4. Exit\n"
        try:
            selected_menu = int(input(menu))
            match selected_menu:
                case 1:
                    return self.uber_server.sign_out()
                case 2:
                    available_orders = self.uber_server.get_available_orders()
                    print(f"\n{'-'*40}\n\n0. Back to Driver menu")
                    for order in available_orders:
                        print(f"id: {order['id']}. from: {order['start_location']} to: {order['destination']}"
                              f" price: {order['price']} status: {order['order_status']}")
                    selected_id = int(input("Please choose order to execute(use id): "))
                    match selected_id:
                        case 0:
                            pass
                        case _:
                            self.raise_income(selected_id)
                            self.uber_server.execute_order(selected_id)
                    return None
                case 3:
                    print(f"Your income is: {self.amount_of_money}")
                case 4:
                    exit()
        except ValueError:
            return None
