from basic_user import BasicUser

class AnonimUser(BasicUser):
    def draw_menu(self) -> dict:
        menu = f"\n{'-'*40}\n\n1. Sign In\n2. Sign Up\n"
        try:
            selected_menu = int(input(menu))
            match selected_menu:
                case 1:
                    username = input('Please enter your username: ')
                    password = input('Please enter your password: ')
                    return self.uber_server.sign_in(username, password)
                case 2:
                    username = input('Please enter your username: ')
                    password = input('Please enter your password: ')
                    role = input("Please enter your role 'Driver' or 'Passenger': ")
                    return self.uber_server.sign_up(username, password, role)              
        except ValueError:
            return None