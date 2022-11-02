from basic_user import BasicUser

class Passenger(BasicUser):
    def draw_menu(self) -> dict:
        menu = f"\n{'-'*40}\n\nHello Passenger {self.username}\n1. Sign Out\n2. Place an Order\n"
        try:
            selected_menu = int(input(menu))
            match selected_menu:
                case 1:
                    return self.uber_server.sign_out(self.username)
                case 2:
                    start_location = input('Please enter your start location: ')
                    destination = input('Please enter your destination: ')
                    price = input("Please enter your price: ")
                    self.uber_server.create_new_order(self.username, start_location, destination, price)  
                    return None            
        except ValueError:
            return self