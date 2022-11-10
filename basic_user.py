from uber_server import Server
import json


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

