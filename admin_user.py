from basic_user import BasicUser


class AdminUser(BasicUser):

    def draw_menu(self):
        menu = f"\n{'-'*40}\n\nHello Admin {self.username}\n1. See all users\n2. Sign Out\n"
        try:
            selected_menu = int(input(menu))
            match selected_menu:
                case 1:
                    print(self.uber_server.get_all_users())
                    return None
                case 2:
                    return self.uber_server.sign_out()
        except ValueError:
            return None
