import datetime

# Function to read ManufacturerList.txt
def read_manufacturer_list(file_path):
    """
    Reads the ManufacturerList.txt file and returns a dictionary of items.
    Each item contains details like ID, manufacturer, type, and damaged status.
    """
    manufacturer_data = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Split the line by comma and strip whitespace
            parts = [part.strip() for part in line.split(',')]
            item_id = parts[0]
            manufacturer = parts[1]
            item_type = parts[2]
            damaged = parts[3] if len(parts) > 3 else None  # Damaged indicator may be missing
            manufacturer_data[item_id] = {
                'manufacturer': manufacturer,
                'item_type': item_type,
                'damaged': damaged
            }
    return manufacturer_data


# Function to read PriceList.txt
def read_price_list(file_path):
    """
    Reads the PriceList.txt file and returns a dictionary mapping item IDs to prices.
    """
    price_data = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Split the line by comma and strip whitespace
            parts = [part.strip() for part in line.split(',')]
            item_id = parts[0]
            price = float(parts[1])  # Convert price to float
            price_data[item_id] = price
    return price_data


# Function to read ServiceDatesList.txt
def read_service_dates_list(file_path):
    """
    Reads the ServiceDatesList.txt file and returns a dictionary mapping item IDs to service dates.
    """
    service_date_data = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Split the line by comma and strip whitespace
            parts = [part.strip() for part in line.split(',')]
            item_id = parts[0]
            service_date = datetime.datetime.strptime(parts[1], '%m/%d/%Y').date()  # Convert to date object
            service_date_data[item_id] = service_date
    return service_date_data


# Helper function to sort inventory by manufacturer name
def sort_by_manufacturer(inventory):
    """
    Sorts the inventory list alphabetically by manufacturer name.
    """
    for i in range(len(inventory)):
        for j in range(i + 1, len(inventory)):
            if inventory[i]['manufacturer'] > inventory[j]['manufacturer']:
                inventory[i], inventory[j] = inventory[j], inventory[i]
    return inventory


# Helper function to sort inventory by item ID
def sort_by_item_id(inventory):
    """
    Sorts the inventory list by item ID.
    """
    for i in range(len(inventory)):
        for j in range(i + 1, len(inventory)):
            if inventory[i]['item_id'] > inventory[j]['item_id']:
                inventory[i], inventory[j] = inventory[j], inventory[i]
    return inventory


# Helper function to sort inventory by service date (oldest to most recent)
def sort_by_service_date(inventory):
    """
    Sorts the inventory list by service date (oldest to most recent).
    """
    for i in range(len(inventory)):
        for j in range(i + 1, len(inventory)):
            if inventory[i]['service_date'] > inventory[j]['service_date']:
                inventory[i], inventory[j] = inventory[j], inventory[i]
    return inventory


# Helper function to sort inventory by price (most expensive to least expensive)
def sort_by_price(inventory):
    """
    Sorts the inventory list by price (most expensive to least expensive).
    """
    for i in range(len(inventory)):
        for j in range(i + 1, len(inventory)):
            if inventory[i]['price'] < inventory[j]['price']:
                inventory[i], inventory[j] = inventory[j], inventory[i]
    return inventory


# Function to write FullInventory.txt
def write_full_inventory(manufacturer_data, price_data, service_date_data, output_file):
    """
    Writes the FullInventory.txt file with all items sorted alphabetically by manufacturer.
    """
    inventory = []
    for item_id, details in manufacturer_data.items():
        inventory.append({
            'item_id': item_id,
            'manufacturer': details['manufacturer'],
            'item_type': details['item_type'],
            'price': price_data.get(item_id, 0),  # Default to 0 if price is missing
            'service_date': service_date_data.get(item_id, None),
            'damaged': details['damaged']
        })

    # Sort inventory by manufacturer name
    inventory = sort_by_manufacturer(inventory)

    # Write to FullInventory.txt
    with open(output_file, 'w') as file:
        for item in inventory:
            file.write(f"{item['item_id']}, {item['manufacturer']}, {item['item_type']}, "
                       f"{item['price']}, {item['service_date'].strftime('%m/%d/%Y')}, {item['damaged'] or ''}\n")


# Function to write Item Type Inventory files (e.g., LaptopInventory.txt)
def write_item_type_inventories(manufacturer_data, price_data, service_date_data, output_dir):
    """
    Writes separate inventory files for each item type, sorted by item ID.
    """
    item_type_groups = {}
    for item_id, details in manufacturer_data.items():
        item_type = details['item_type']
        if item_type not in item_type_groups:
            item_type_groups[item_type] = []
        item_type_groups[item_type].append({
            'item_id': item_id,
            'manufacturer': details['manufacturer'],
            'price': price_data.get(item_id, 0),
            'service_date': service_date_data.get(item_id, None),
            'damaged': details['damaged']
        })

    # For each item type, sort by item ID and write to file
    for item_type, items in item_type_groups.items():
        items = sort_by_item_id(items)  # Sort by item ID
        file_name = f"{output_dir}/{item_type.capitalize()}Inventory.txt"
        with open(file_name, 'w') as file:
            for item in items:
                file.write(f"{item['item_id']}, {item['manufacturer']}, {item['price']}, "
                           f"{item['service_date'].strftime('%m/%d/%Y')}, {item['damaged'] or ''}\n")


# Function to write PastServiceDateInventory.txt
def write_past_service_date_inventory(manufacturer_data, price_data, service_date_data, output_file):
    """
    Writes the PastServiceDateInventory.txt file with items past their service date.
    """
    today = datetime.date.today()
    past_service_items = []

    for item_id, details in manufacturer_data.items():
        service_date = service_date_data.get(item_id, None)
        if service_date and service_date < today:  # Check if service date is in the past
            past_service_items.append({
                'item_id': item_id,
                'manufacturer': details['manufacturer'],
                'item_type': details['item_type'],
                'price': price_data.get(item_id, 0),
                'service_date': service_date,
                'damaged': details['damaged']
            })

    # Sort by service date (oldest to most recent)
    past_service_items = sort_by_service_date(past_service_items)

    # Write to PastServiceDateInventory.txt
    with open(output_file, 'w') as file:
        for item in past_service_items:
            file.write(f"{item['item_id']}, {item['manufacturer']}, {item['item_type']}, "
                       f"{item['price']}, {item['service_date'].strftime('%m/%d/%Y')}, {item['damaged'] or ''}\n")


# Function to write DamagedInventory.txt
def write_damaged_inventory(manufacturer_data, price_data, service_date_data, output_file):
    """
    Writes the DamagedInventory.txt file with all damaged items.
    """
    damaged_items = []

    for item_id, details in manufacturer_data.items():
        if details['damaged']:  # Check if the item is damaged
            damaged_items.append({
                'item_id': item_id,
                'manufacturer': details['manufacturer'],
                'item_type': details['item_type'],
                'price': price_data.get(item_id, 0),
                'service_date': service_date_data.get(item_id, None)
            })

    # Sort by price (most expensive to least expensive)
    damaged_items = sort_by_price(damaged_items)

    # Write to DamagedInventory.txt
    with open(output_file, 'w') as file:
        for item in damaged_items:
            file.write(f"{item['item_id']}, {item['manufacturer']}, {item['item_type']}, "
                       f"{item['price']}, {item['service_date'].strftime('%m/%d/%Y')}\n")


# Main function to execute the program
def main():
    # Input file paths
    manufacturer_list_file = 'ManufacturerList.txt'
    price_list_file = 'PriceList.txt'
    service_dates_list_file = 'ServiceDatesList.txt'

    # Output file paths
    full_inventory_file = 'FullInventory.txt'
    past_service_date_file = 'PastServiceDateInventory.txt'
    damaged_inventory_file = 'DamagedInventory.txt'
    output_dir = '.'  # Current directory for item type inventory files

    # Read input files
    manufacturer_data = read_manufacturer_list(manufacturer_list_file)
    price_data = read_price_list(price_list_file)
    service_date_data = read_service_dates_list(service_dates_list_file)

    # Generate output files
    write_full_inventory(manufacturer_data, price_data, service_date_data, full_inventory_file)
    write_item_type_inventories(manufacturer_data, price_data, service_date_data, output_dir)
    write_past_service_date_inventory(manufacturer_data, price_data, service_date_data, past_service_date_file)
    write_damaged_inventory(manufacturer_data, price_data, service_date_data, damaged_inventory_file)


if __name__ == '__main__':
    main()