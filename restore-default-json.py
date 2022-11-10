import json

default_database = {
    "admin": {
        "username": "admin",
        "password": "12345",
        "role": "Admin"
    },
    "ana": {
        "username": "ana",
        "password": "12345",
        "role": "Passenger",
        "amount_of_money": "0",
        "online_status": False
    },
    "edystang": {
        "username": "edystang",
        "password": "123456",
        "role": "Passenger",
        "amount_of_money": "0",
        "online_status": False
    },
    "edy_the_driver": {
        "username": "edy_the_driver",
        "password": "123456",
        "role": "Driver",
        "amount_of_money": "0",
        "rating": 0,
        "number_of_ratings": 0,
        "online_status": False
    }
}

with open('database.json', 'w') as jsonfile:
    json.dump(default_database, jsonfile, indent=4)

default_database_orders = [
    {
        "id": 1,
        "start_location": "home",
        "username": "ana",
        "destination": "jim",
        "price": "14",
        "order_status": "created",
        "is_rated": "unrated"
    },
    {
        "id": 2,
        "start_location": "home",
        "username": "ana",
        "destination": "university",
        "price": 40,
        "order_status": "created",
        "is_rated": "unrated"
},
    {
        "id": 3,
        "start_location": "home",
        "username": "edystang",
        "destination": "work",
        "price": 77,
        "order_status": "created",
        "is_rated": "unrated"
    },
    {
        "id": 4,
        "start_location": "city",
        "username": "edystang",
        "destination": "mistress",
        "price": 5,
        "order_status": "executed",
        "is_rated": "rated",
        "driver_username": "edy_the_driver"
    },
]

with open('remember_last_order_id.txt', 'w') as last_id_file:
    last_id_file.write('4')

with open('database_orders.json', 'w') as jsonfile:
    json.dump(default_database_orders, jsonfile, indent=4)

default_database_help_desk = [
    {
        "id": 1,
        "username": "edy_the_driver",
        "role": "Driver",
        "title": "emergency",
        "message": "we need more drivers",
        "seen": "no"
    },
    {
        "id": 2,
        "username": "edystang",
        "role": "Passenger",
        "title": "review",
        "message": "Great app so far",
        "seen": "no"
    }
]

with open('remember_last_msg_id.txt', 'w') as last_id_file:
    last_id_file.write('2')

with open('database_help_desk.json', 'w') as jsonfile:
    json.dump(default_database_help_desk, jsonfile, indent=4)
