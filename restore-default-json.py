import json

default_database = {
    "admin": {
        "username": "admin",
        "password": "12345",
        "role": "Admin"
    },
    "vova": {
        "username": "vova",
        "password": "12345",
        "role": "Driver"
    },
    "ana": {
        "username": "ana",
        "password": "12345",
        "role": "Passenger"
    },
    "edystang": {
        "username": "edystang",
        "password": "123456",
        "role": "Passenger"
    },
    "edy_the_driver": {
        "username": "edy_the_driver",
        "password": "123456",
        "role": "Driver"
    }
}

with open('database.json', 'w') as jsonfile:
    json.dump(default_database, jsonfile, indent=4)

default_database_orders = [
    {
        "start_location": "home",
        "username": "ana",
        "destination": "jim",
        "price": "14",
        "order_status": "executed"
    },
    {
        "start_location": "home",
        "username": "ana",
        "destination": "university",
        "price": "40",
        "order_status": "created"
    },
    {
        "start_location": "home",
        "username": "edystang",
        "destination": "work",
        "price": "77",
        "order_status": "executed"
    }
]

with open('database_orders.json', 'w') as jsonfile:
    json.dump(default_database_orders, jsonfile, indent=4)
