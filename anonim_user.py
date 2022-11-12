from basic_user import BasicUser


class AnonimUser(BasicUser):
    def draw_menu(self):
        menu = f"\n{'-'*40}\n\n1. Sign In\n2. Sign Up\n3. Exit\n"
        try:
            selected_menu = int(input(menu))
            match selected_menu:
                case 1:
                    username = input('Please enter your username: ')
                    password = input('Please enter your password: ')
                    return self.uber_server.sign_in(username, password)
                case 2:
                    role = input("Please enter your role 'Driver' or 'Passenger': ")
                    username = input('Please enter your username: ')
                    all_users_dicts = self.uber_server.get_all_users()
                    while username in all_users_dicts:
                        username = input('That username already exists. Please enter another username: ')
                    password = self.password_generator()
                    return self.uber_server.sign_up(username, password, role)
                case 3:
                    exit()
        except ValueError:
            return None
