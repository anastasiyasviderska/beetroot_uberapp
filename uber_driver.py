from basic_user import BasicUser


class Driver(BasicUser):
    def draw_menu(self):
        menu = f"\n{'-'*40}\n\nHello Driver {self.username}\n1. Sign Out\n2. Available Orders\n"
        try:
            selected_menu = int(input(menu))
            match selected_menu:
                case 1:
                    return self.uber_server.sign_out(self.username)
                case 2:
                    available_orders = self.uber_server.get_available_orders()
                    print(f"\n{'-'*40}\n\n1. Back to Driver menu")
                    for index, order in enumerate(available_orders):
                        print(f"{index + 2}. from: {order['start_location']} to: {order['destination']} price: {order['price']} status: {order['order_status']}")
                    selected_index = int(input("Please choose order to execute(use index): "))
                    match selected_index:
                        case 1:
                            pass
                        case _:
                            selected_order = available_orders[selected_index - 2]
                            self.uber_server.execute_order(selected_order['username'],selected_order['start_location'], selected_order['destination'], selected_order['price'])
                    return None        
        except ValueError:
            return None
