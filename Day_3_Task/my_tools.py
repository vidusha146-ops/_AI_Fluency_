def find_lost_item(item_name):
    lost_items = {
        "black water bottle": {
            "location": "Library 2nd Floor",
            "status": "Found"
        },
        "blue umbrella": {
            "location": "College Canteen",
            "status": "Found"
        },
        "scientific calculator": {
            "location": "Block C Lab",
            "status": "Found"
        },
        "black usb drive": {
            "location": "Seminar Hall",
            "status": "Found"
        },
        "student id card": {
            "location": "Main Office",
            "status": "Found"
        }
    }

    item_name = item_name.lower().strip()

    if item_name in lost_items:
        item = lost_items[item_name]

        return (
            f"Item: {item_name.title()}\n"
            f"Location: {item['location']}\n"
            f"Status: {item['status']}"
        )

    return f"No matching item was found for '{item_name}'."


if __name__ == "__main__":
    print(find_lost_item("black water bottle"))
    print()
    print(find_lost_item("scientific calculator"))
    print()
    print(find_lost_item("red smartwatch"))