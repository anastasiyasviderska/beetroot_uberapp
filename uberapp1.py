import json


class Customer:
    def __init__(self):
        self.username = None
        self.password = None

    def sign_up(self):
        self.username = input("Please enter your username: ")
        self.password = input("Please enter your password: ")
        login_data = {"username": self.username,
                      "password": self.password}

        with open('login_information.json') as outfile:
            file_obj = json.load(outfile)

        file_obj.append(login_data)

        with open('login_information.json', 'w') as outfile:
            json.dump(file_obj, outfile, indent=4)
        pass

    @staticmethod
    def sign_in():
        writen_username = input('Username: ')
        writen_password = input('Password: ')
        with open('login_information.json', 'r') as outfile:
            login_details_list = json.load(outfile)

        for dictionary in login_details_list:
            if dictionary["username"] == writen_username and dictionary["password"] == writen_password:
                return True

        print('No such user or password. Create new account or write your login data properly.')


class BasicUser(Customer):
    pass


class Driver(Customer):
    pass