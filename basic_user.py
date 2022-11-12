from uber_server import Server
import json
from random_password_generator import random_password_generator


class BasicUser:

    uber_server = Server('database')

    def __init__(self):
        self.username = None
        self.password = None
        self.amount_of_money = 0

    def __repr__(self) -> str:
        return f"name: {self.username}"

    def draw_menu(self) -> dict:
        pass

    def update_money_in_db(self):
        with open('database.json', 'r+') as users_db:
            data = json.load(users_db)
            data[self.username]['amount_of_money'] = str(self.amount_of_money)
            users_db.seek(0)
            json.dump(data, users_db, indent=4)
            users_db.truncate()

    def send_message_to_helpdesk(self, user_role):
        print("Welcome to our Uber Help Desk!")
        new_title = input("Please type the message's title!\n")
        new_message = input("Please type your message so that our administrators can help you!\n")
        self.uber_server.create_new_message(self.username, user_role, new_title, new_message)

    @staticmethod
    def password_generator():
        password_type = input('Do you want a randomly generated password? (y/n): ')
        while password_type not in ['y', 'n']:
            password_type = input('You entered an invalid option. Please, choose "y" or "n": ')
        match password_type:
            case 'n':
                while True:
                    password = input('Please enter your new password (4-16 characters): ')
                    if len(password) < 4:
                        print('Your password is too short!')
                        continue
                    if len(password) > 16:
                        print('Your password is too long!')
                        continue

                    password_confirmation = input('Please confirm your password: ')
                    if password != password_confirmation:
                        print('Your passwords do not match! Please, try again.')
                        continue
                    return password

            case 'y':
                return random_password_generator()

    def change_password(self):
        password_identification = input('Please enter your password to continue or press "0" to go back: ')
        match password_identification:
            case 0:
                return None
            case _:
                with open('database.json', 'r+') as users_db:
                    data = json.load(users_db)
                    if data[self.username]['password'] == password_identification:
                        data[self.username]['password'] = self.password_generator()
                        users_db.seek(0)
                        json.dump(data, users_db, indent=4)
                        users_db.truncate()
                    else:
                        print('The password you entered is incorrect.')
                        return None

    def open_help_desk(self):
        try:
            choose_new_action = input(f"\n{'-' * 40}\n\n0. Go back\n1. Write a new message\n"
                                      f"2. See messages sent\n")
            match int(choose_new_action):
                case 0:
                    return None
                case 1:
                    with open('database.json', 'r') as users_db:
                        data = json.load(users_db)
                        self.send_message_to_helpdesk(data[self.username]['role'])
                case 2:
                    user_msg = self.uber_server.get_user_messages(self.username)
                    for msg in user_msg:
                        print(f"Message id: {msg['id']}\n"
                              f"From: {msg['username']}\n"
                              f"Title: {msg['title']}\n"
                              f"Message: {msg['message']}\n\n")
        except TypeError:
            return None
