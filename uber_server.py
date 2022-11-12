import json


class Server:
    def __init__(self, db_path: str) -> None:
        self.main_db_path = db_path + '.json'
        self.orders_db_path = db_path + '_orders.json'
        self.help_desk_db_path = db_path + '_help_desk.json'
        # this helps the app keep the track of ids in database.json
        with open('remember_last_order_id.txt') as last_order_id_file:
            self.id_iter = int(last_order_id_file.read())
        with open('remember_last_msg_id.txt') as last_msg_id_file:
            self.message_id = int(last_msg_id_file.read())

    def sign_in(self, login: str, password: str):
        print(f"searching user with login: {login}")
        users = self.read_db()
        if login in users:
            user_dict = users[login]
            if password == user_dict['password']:
                user_dict['online_status'] = True
                self.write_db(user_dict)
                # if user_dict['role'] == 'Driver':
                #     print(f"Your rating is {user_dict['rating']}")
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
        elif role == "Passenger":
            user = {'username': username, 'password': password, 'role': role,
                    'amount_of_money': 0, 'online_status': True}
        else:
            user = {'username': username, 'password': password, 'role': role,
                    'online_status': True}
        self.write_db(user)
        return user

    # INTERACT WITH USERS
    def get_all_users(self) -> dict:
        return self.read_db()

    def get_online_users(self) -> dict:
        online_users = self.read_db()
        return dict(
            filter(lambda user: user[1]['online_status'] == True and user[1]['role'] != 'Admin', online_users.items()))

    def sign_out(self, login):
        users = self.read_db()
        if login in users:
            user_dict = users[login]
            user_dict['online_status'] = False
            self.write_db(user_dict)
        return {'role': 'Anonim'}

    def delete_user(self, username):
        pass

    # ORDERS
    def create_new_order(self, username: str, start_location: str, destination: str, price: str) -> None:
        self.id_iter += 1
        with open('remember_last_order_id.txt', 'w') as last_id_file:
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
            return {}

    # WORK WITH USERS DATABASE
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

    # WORK WITH HELP DESK MESSAGES
    def write_help_desk_db(self, message: dict):
        try:
            with open(self.help_desk_db_path, 'r+') as help_desk:
                data = json.load(help_desk)
                data.append(message)
                help_desk.seek(0)
                json.dump(data, help_desk, indent=4)
                help_desk.truncate()
        except FileNotFoundError:
            with open(self.help_desk_db_path, 'w') as file_object:
                json.dump([dict], file_object, indent=4)
            return {}

    def create_new_message(self, username, user_role, user_title, user_message) -> None:
        self.message_id += 1
        with open('remember_last_msg_id.txt', 'w') as last_msg_id_file:
            last_msg_id_file.write(str(self.message_id))
        self.write_message_db({'id': self.message_id,
                               'username': username,
                               'role': user_role,
                               'title': user_title,
                               'message': user_message,
                               'seen': 'no'
                               })
    
    def read_msg_db(self):
        try:
            with open(self.help_desk_db_path) as help_desk:
                log_det = json.load(help_desk)
                return log_det
        except FileNotFoundError:
            with open(self.help_desk_db_path, 'w') as help_desk:
                json.dump({}, help_desk, indent=4)
            return {}

    def get_unseen_messages(self):
        all_messages = self.read_msg_db()
        return list(filter(lambda msg: msg['seen'] == 'no', all_messages))

    def get_user_messages(self, username):
        all_messages = self.read_msg_db()
        return list(filter(lambda msg: msg['username'] == username, all_messages))

    def write_message_db(self, message: dict):
        try:
            with open(self.help_desk_db_path, 'r+') as help_desk:
                data = json.load(help_desk)
                data.append(message)
                help_desk.seek(0)
                json.dump(data, help_desk, indent=4)
                help_desk.truncate()
            help_desk.close()
        except FileNotFoundError:
            with open(self.orders_db_path, 'w') as help_desk:
                json.dump([dict], help_desk, indent=4)
            return {}
        
    def mark_message_as_seen(self, id: int) -> None:
        with open(self.help_desk_db_path, 'r+') as help_desk:
            data = json.load(help_desk)
            for msg_dict in data:
                if msg_dict['id'] == id:
                    msg_dict['seen'] = 'yes'
            help_desk.seek(0)
            json.dump(data, help_desk, indent=4)
            help_desk.truncate()
        help_desk.close()
