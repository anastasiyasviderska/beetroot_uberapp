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

    def raise_income(self, id):
        with open('database_orders.json', 'r') as database_orders_file:
            data = json.load(database_orders_file)
            for order_dict in data:
                if order_dict['id'] == id:
                    self.amount_of_money += int(order_dict['price'])

        with open('database.json', 'r+') as database_file:
            data = json.load(database_file)
            data[self.username]['amount_of_money'] = str(self.amount_of_money)
            database_file.seek(0)
            json.dump(data, database_file, indent=4)
            database_file.truncate()
