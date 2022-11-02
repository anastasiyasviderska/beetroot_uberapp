from basic_user import BasicUser

class Driver(BasicUser):
    def draw_menu(self) -> dict:
        menu = f"\n{'-'*40}\n\nHello Driver {self.username}\n1. Sign Out\n2. \n"
        try:
            selected_menu = int(input(menu))
            match selected_menu:
                case 1:
                    return self.uber_server.sign_out(self.username)
                case 2:
                    username = input('Please enter your username: ')
                    password = input('Please enter your password: ')
                    role = input("Please enter your role 'Driver' or 'Passenger': ")
                    return uber_server1.sign_up(username, password, role)              
        except ValueError:
            return self