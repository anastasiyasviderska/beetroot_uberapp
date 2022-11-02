
from basic_user import BasicUser
from anonim_user import AnonimUser
from uber_server import Server
from uber_passenger import Passenger
from uber_driver import Driver
from admin_user import AdminUser             

user = AnonimUser()
    
while True:
    user_dict = user.draw_menu()
    print(user_dict)
    if not user_dict is None:
        match user_dict['role']:
            case 'Driver':
                user = Driver()
                user.password = user_dict['password']
                user.username = user_dict['username']
            case 'Passenger':
                user = Passenger()
                user.password = user_dict['password']
                user.username = user_dict['username']
            case 'Admin':
                user = AdminUser()
                user.password = user_dict['password']
                user.username = user_dict['username']
            case _:
                user = AnonimUser()


