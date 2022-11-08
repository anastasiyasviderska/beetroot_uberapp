import json


class Server:
    def __init__(self, db_path: str) -> None:
        self.main_db_path = db_path + '.json'
        self.orders_db_path = db_path + '_orders.json'
        with open('remember_last_id.txt') as last_id_file:
            self.id_iter = int(last_id_file.read())

    def sign_in(self, login: str, password: str):
        print(f"searching user with login: {login}")
        users = self.read_db()
        if login in users:
            user_dict = users[login]
            if password == user_dict['password']:
                user_dict['online_status'] = True
                self.write_db(user_dict)
                print(f"Found: {user_dict}")
                return user_dict
            else:
                print("Your Password is Incorrect")
        else:
            print("Login does not exist")
        return None

    def sign_up(self, username: str, password: str, role: str) -> dict:
        if role == 'Driver':
            user = {'username': username, 'password': password, 'role': role,
                    'amount_of_money': 0, 'rating_sum': 0, 'rating': 0, 'online_status': True}
        else:
            user = {'username': username, 'password': password, 'role': role,
                    'amount_of_money': 0, 'online_status': True}
        self.write_db(user)
        return user

    def get_all_users(self) -> dict:
        return self.read_db()
    
    def get_online_users(self) -> dict:
        online_users = self.read_db()
        return dict(filter(lambda user: user[1]['online_status'] == True and user[1]['role'] != 'Admin', online_users.items()))

    def sign_out(self, login):
        users = self.read_db()
        if login in users:
            user_dict = users[login]
            user_dict['online_status'] = False
            self.write_db(user_dict)
        return {'role': 'Anonim'}

    def create_new_order(self, username: str, start_location: str, destination: str, price: str) -> None:
        self.id_iter += 1
        with open('remember_last_id.txt', 'w') as last_id_file:
            last_id_file.write(str(self.id_iter))
        self.write_order_db({'id': self.id_iter, 'start_location': start_location, 'username': username,
                             'destination': destination, 'price': price, 'order_status': 'created',
                             'is_rated': 'unrated'})

    def get_user_orders(self, username: str) -> list:
        all_orders = self.read_order_db()
        list_of_orders = list(filter(lambda order: order['username'] == username, all_orders))
        list_of_orders.reverse()
        return list_of_orders

    def get_available_orders(self) -> list:
        all_orders = self.read_order_db()
        return list(filter(lambda order: order['order_status'] == 'created', all_orders))
    
    def delete_user(self, username):
        pass

    def execute_order(self, id: int, driver_username: str) -> None:
        with open(self.orders_db_path, 'r+') as file_object:
            data = json.load(file_object)
            for order_dict in data:
                if order_dict['id'] == id:
                    order_dict['order_status'] = 'executed'
                    order_dict['driver_username'] = driver_username
            file_object.seek(0)
            json.dump(data, file_object, indent=4)
            file_object.truncate()
        file_object.close()

    def get_executed_orders(self, username) -> list:
        all_orders = self.read_order_db()
        return list(filter(lambda order: order['order_status'] == 'executed'
                                         and (order['driver_username'] == username
                                              or order['username'] == username), all_orders))


    def read_db(self) -> dict:
        try:
            with open(self.main_db_path) as file_object:
                log_det = json.load(file_object)
                return log_det
        except FileNotFoundError:
            with open(self.main_db_path, 'w') as file_object:
                json.dump({}, file_object, indent=4)
            file_object.close()
            return {}

    def write_db(self, user: dict) -> None:
        with open(self.main_db_path, 'r+') as file_object:
            data = json.load(file_object)
            data[user['username']] = user
            file_object.seek(0)
            json.dump(data, file_object, indent=4)
            file_object.truncate()

    def delete_db_item(self, username: str) -> None:
        with open(self.main_db_path, 'r+') as file_object:
            data = json.load(file_object)
            data.pop(username)
            file_object.seek(0)
            json.dump(data, file_object, indent=4)
            file_object.truncate()


    def read_order_db(self):
        try:
            with open(self.orders_db_path) as file_object:
                log_det = json.load(file_object)
                return log_det
        except FileNotFoundError:
            with open(self.orders_db_path, 'w') as file_object:
                json.dump({}, file_object, indent=4)
            file_object.close()
            return {}

    def write_order_db(self, order: dict):
        try:
            with open(self.orders_db_path, 'r+') as file_object:
                data = json.load(file_object)
                data.append(order)
                file_object.seek(0)
                json.dump(data, file_object, indent=4)
                file_object.truncate()
            file_object.close()
        except FileNotFoundError:
            with open(self.orders_db_path, 'w') as file_object:
                json.dump([dict], file_object, indent=4)
            file_object.close()
            return {}


