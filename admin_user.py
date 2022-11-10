from basic_user import BasicUser


class AdminUser(BasicUser):

    def draw_menu(self):
        menu = f"\n{'-'*40}\n\nHello Admin {self.username}\n1. See all users\n2. Delete User\n" \
               f"3. Open Help Desk\n4. Sign Out\n5. Exit \n"
        try:
            selected_menu = int(input(menu))
            match selected_menu:
                case 1:
                    print(f"\n{'-' * 40}\n")
                    users = self.uber_server.get_all_users()
                    for user in users.values():
                        print(f"username: {user['username']} role: {user['role']} "
                              f"status: {'online' if user['online_status'] else 'offline'}")
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
                    admin_choice = int(input(f"\n{'-'*40}\n\n1. Return to menu\n2. See all messages!\n"))
                    match admin_choice:
                        case 1:
                            return None
                        case 2:
                            print("You'll see all available messages!")
                            all_messages = self.uber_server.get_unseen_messages()
                            list_of_ids = []
                            for message in all_messages:
                                list_of_ids.append(message['id'])
                                print(f"id: {message['id']}, author: {message['username']}, title: {message['title']}")
                            chosen_id = ''
                            while chosen_id not in list_of_ids:
                                chosen_id = int(input("Please choose a message to read, based on its id: "))
                            for message in all_messages:
                                if message['id'] == chosen_id:
                                    self.uber_server.mark_message_as_seen(chosen_id)
                                    print(f"Message id: {message['id']}\n"
                                          f"From: {message['username']}\n"
                                          f"Title: {message['title']}\n"
                                          f"Message: {message['message']}")
                            return None
                case 4:
                    return self.uber_server.sign_out(self.username)
                case 5:
                    exit()
        except ValueError:
            return None
