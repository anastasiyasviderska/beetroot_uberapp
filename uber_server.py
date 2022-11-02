import json


class Server:
    def __init__(self, db_path: str) -> None:
        self.main_db_path = db_path + '.json'
        self.orders_db_path = db_path + '_orders.json'
    
    def sign_in(self, login: str, password: str) -> dict:
        print(f"searching user with login: {login}")
        users = self.read_db()
        if login in users:
            user_dict = users[login]
            if password == user_dict['password']:
                print(f"Found: {user_dict}")
                return user_dict
            else:
                print("Your Password is Incorrect")
        else:
            print("Login does not exist")
        return None

    def sign_up(self, username: str, password: str, role: str) -> dict:
        user = {'username': username, 'password': password, 'role': role}
        self.write_db(user)
        return user

    def get_all_users(self) -> dict:
        return self.read_db()
    
    def sign_out(self, username: str) -> dict:
        return {'role': 'Anonim'}
    
    def create_new_order(self, username: str, start_location: str, destination: str, price: str) -> None:
        self.write_order_db({'start_location': start_location, 'username': username, 'destination': destination, 'price': price, 'order_status': 'created'})
    
    def get_user_orders(self, username: str) -> list:
        all_orders = self.read_order_db()
        return list(filter(lambda order: order['username'] == username, all_orders))
        
    def get_available_orders(self) -> list:
        all_orders = self.read_order_db()
        return list(filter(lambda order: order['order_status'] == 'created', all_orders))
    
    def execute_order(self, username: str, start_location: str, destination: str, price: str) -> None:
        with open (self.orders_db_path, 'r+') as file_object:
            data = json.load(file_object)
            for order_dict in data:
                if order_dict['username'] == username and order_dict['start_location'] == start_location and order_dict['destination'] == destination and order_dict['price'] == price:
                    order_dict['order_status'] = 'executed'
            file_object.seek(0)
            json.dump(data, file_object)
            file_object.truncate()
        file_object.close()


    def read_db(self) -> dict:
        try:
            with open (self.main_db_path) as file_object:
                log_det = json.load(file_object)
                return log_det
        except FileNotFoundError:
            with open (self.main_db_path, 'w') as file_object:
                json.dump({}, file_object)
            file_object.close()
            return {}

    def write_db(self, user: dict) -> None:
        with open (self.main_db_path, 'r+') as file_object:
            data = json.load(file_object)
            data[user['username']] = user
            file_object.seek(0)
            json.dump(data, file_object)
            file_object.truncate()
        file_object.close()

    def read_order_db(self) -> list:
        try:
            with open(self.orders_db_path) as file_object:
                log_det = json.load(file_object)
                return log_det
        except FileNotFoundError:
            with open (self.orders_db_path, 'w') as file_object:
                json.dump({}, file_object)
            file_object.close()
            return {}

    def write_order_db(self, order: dict) -> None:
        try:
            with open (self.orders_db_path, 'r+') as file_object:
                data = json.load(file_object)
                data.append(order)
                file_object.seek(0)
                json.dump(data, file_object)
                file_object.truncate()
            file_object.close()
        except FileNotFoundError:
            with open (self.orders_db_path, 'w') as file_object:
                json.dump([dict], file_object)
            file_object.close()
            return {}

