from basic_user import BasicUser


class AdminUser(BasicUser):

    def draw_menu(self):
        menu = f"\n{'-'*40}\n\nHello Admin {self.username}\n1. See all users\n2. Delete User\n3. Sign Out\n"
        try:
            selected_menu = int(input(menu))
            match selected_menu:
                case 1:
                    print(f"\n{'-' * 40}\n")
                    users = self.uber_server.get_all_users()
                    for user in users.values():
                        print(f"username: {user['username']} role: {user['role']} status: {'online' if user['online_status'] else 'offline'}")
                    return None
                case 2:
                    user_dict = self.uber_server.get_online_users()
                    print(f"\n{'-' * 40}\n")
                    for user in user_dict.values():
                        print(f"username: {user['username']}. role: {user['role']}")
                    delete_username = input("\nPlease enter a username to delete: ")
                    self.uber_server.delete_db_item(delete_username)
                    print(f"\nUser {delete_username} was deleted successfully")
                    return None
                case 3:
                    return self.uber_server.sign_out(self.username)
        except ValueError:
            return None
