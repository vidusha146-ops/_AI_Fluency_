def get_travel_information(option):

    travel_data = {
        "A": {
            "cost": 180,
            "time": 80
        },
        "B": {
            "cost": 250,
            "time": 60
        }
    }

    return travel_data.get(option)