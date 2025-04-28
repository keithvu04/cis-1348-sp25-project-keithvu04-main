import datetime
import os

# Inventory Class
class Inventory:
    def __init__(self):
        """Initialize inventory data structures"""
        self.manufacturer_data = {}
        self.price_data = {}
        self.service_date_data = {}

    def read_manufacturer_list(self, file_path):
        """Read ManufacturerList.txt and load manufacturer data"""
        with open(file_path, 'r') as file:
            for line in file:
                parts = [part.strip() for part in line.split(',')]
                item_id = parts[0]
                manufacturer = parts[1]
                item_type = parts[2]
                damaged = parts[3] if len(parts) > 3 else None
                self.manufacturer_data[item_id] = {
                    'manufacturer': manufacturer,
                    'item_type': item_type,
                    'damaged': damaged
                }

    def read_price_list(self, file_path):
        """Read PriceList.txt and load price data"""
        with open(file_path, 'r') as file:
            for line in file:
                parts = [part.strip() for part in line.split(',')]
                item_id = parts[0]
                price = float(parts[1])
                self.price_data[item_id] = price

    def read_service_dates_list(self, file_path):
        """Read ServiceDatesList.txt and load service date data"""
        with open(file_path, 'r') as file:
            for line in file:
                parts = [part.strip() for part in line.split(',')]
                item_id = parts[0]
                service_date = datetime.datetime.strptime(parts[1], '%m/%d/%Y').date()
                self.service_date_data[item_id] = service_date

    def write_full_inventory(self, output_file):
        """Write FullInventory.txt sorted by manufacturer name"""
        inventory = []
        for item_id, details in self.manufacturer_data.items():
            inventory.append({
                'item_id': item_id,
                'manufacturer': details['manufacturer'],
                'item_type': details['item_type'],
                'price': self.price_data.get(item_id, 0),
                'service_date': self.service_date_data.get(item_id, None),
                'damaged': details['damaged']
            })

        inventory = sorted(inventory, key=lambda x: x['manufacturer'])

        with open(output_file, 'w') as file:
            for item in inventory:
                file.write(f"{item['item_id']}, {item['manufacturer']}, {item['item_type']}, "
                           f"{item['price']}, {item['service_date'].strftime('%m/%d/%Y')}, {item['damaged'] or ''}\n")

    def write_item_type_inventories(self, output_dir):
        """Write separate inventory files for each item type"""
        item_type_groups = {}
        for item_id, details in self.manufacturer_data.items():
            item_type = details['item_type']
            if item_type not in item_type_groups:
                item_type_groups[item_type] = []
            item_type_groups[item_type].append({
                'item_id': item_id,
                'manufacturer': details['manufacturer'],
                'price': self.price_data.get(item_id, 0),
                'service_date': self.service_date_data.get(item_id, None),
                'damaged': details['damaged']
            })

        for item_type, items in item_type_groups.items():
            items = sorted(items, key=lambda x: x['item_id'])
            file_name = os.path.join(output_dir, f"{item_type.capitalize()}Inventory.txt")
            with open(file_name, 'w') as file:
                for item in items:
                    file.write(f"{item['item_id']}, {item['manufacturer']}, {item['price']}, "
                               f"{item['service_date'].strftime('%m/%d/%Y')}, {item['damaged'] or ''}\n")

    def write_past_service_date_inventory(self, output_file):
        """Write PastServiceDateInventory.txt with expired service dates"""
        today = datetime.date.today()
        past_service_items = []

        for item_id, details in self.manufacturer_data.items():
            service_date = self.service_date_data.get(item_id, None)
            if service_date and service_date < today:
                past_service_items.append({
                    'item_id': item_id,
                    'manufacturer': details['manufacturer'],
                    'item_type': details['item_type'],
                    'price': self.price_data.get(item_id, 0),
                    'service_date': service_date,
                    'damaged': details['damaged']
                })

        past_service_items = sorted(past_service_items, key=lambda x: x['service_date'])

        with open(output_file, 'w') as file:
            for item in past_service_items:
                file.write(f"{item['item_id']}, {item['manufacturer']}, {item['item_type']}, "
                           f"{item['price']}, {item['service_date'].strftime('%m/%d/%Y')}, {item['damaged'] or ''}\n")

    def write_damaged_inventory(self, output_file):
        """Write DamagedInventory.txt with all damaged items"""
        damaged_items = []

        for item_id, details in self.manufacturer_data.items():
            if details['damaged']:
                damaged_items.append({
                    'item_id': item_id,
                    'manufacturer': details['manufacturer'],
                    'item_type': details['item_type'],
                    'price': self.price_data.get(item_id, 0),
                    'service_date': self.service_date_data.get(item_id, None)
                })

        damaged_items = sorted(damaged_items, key=lambda x: -x['price'])

        with open(output_file, 'w') as file:
            for item in damaged_items:
                file.write(f"{item['item_id']}, {item['manufacturer']}, {item['item_type']}, "
                           f"{item['price']}, {item['service_date'].strftime('%m/%d/%Y')}\n")

    def query_inventory(self):
        """User query functionality to search inventory"""
        print("\nWelcome to the Inventory Query System! (Enter 'q' to quit)\n")
        today = datetime.date.today()

        while True:
            user_input = input("Please enter manufacturer and item type: ").strip().lower()
            if user_input == 'q':
                break

            words = user_input.split()
            found_items = []

            # Identify valid manufacturers and item types
            manufacturers = {details['manufacturer'].lower() for details in self.manufacturer_data.values()}
            item_types = {details['item_type'].lower() for details in self.manufacturer_data.values()}

            # Extract manufacturer and item type from user input
            input_manufacturers = [word for word in words if word in manufacturers]
            input_item_types = [word for word in words if word in item_types]

            # Validation: must be exactly 1 manufacturer and 1 item type
            if len(input_manufacturers) != 1 or len(input_item_types) != 1:
                print("No such item in inventory\n")
                continue

            manufacturer = input_manufacturers[0]
            item_type = input_item_types[0]

            # Find matching items
            for item_id, details in self.manufacturer_data.items():
                if (details['manufacturer'].lower() == manufacturer and
                        details['item_type'].lower() == item_type and
                        not details['damaged']):
                    service_date = self.service_date_data.get(item_id, today)
                    if service_date >= today:
                        found_items.append({
                            'item_id': item_id,
                            'manufacturer': details['manufacturer'],
                            'item_type': details['item_type'],
                            'price': self.price_data.get(item_id, 0)
                        })

            if not found_items:
                print("No such item in inventory\n")
                continue

            # Select the most expensive item
            selected_item = max(found_items, key=lambda x: x['price'])
            print(f"Your item is: {selected_item['item_id']}, {selected_item['manufacturer']}, "
                  f"{selected_item['item_type']}, {selected_item['price']}")

            # Find alternative item (different manufacturer but same item type)
            alternatives = []
            for item_id, details in self.manufacturer_data.items():
                if (details['item_type'].lower() == item_type and
                        details['manufacturer'].lower() != manufacturer and
                        not details['damaged']):
                    service_date = self.service_date_data.get(item_id, today)
                    if service_date >= today:
                        alternatives.append({
                            'item_id': item_id,
                            'manufacturer': details['manufacturer'],
                            'item_type': details['item_type'],
                            'price': self.price_data.get(item_id, 0)
                        })

            if alternatives:
                # Find closest price alternative
                alt_item = min(alternatives, key=lambda x: abs(x['price'] - selected_item['price']))
                print(f"You may, also, consider: {alt_item['item_id']}, {alt_item['manufacturer']}, "
                      f"{alt_item['item_type']}, {alt_item['price']}")
            print()

# --- Main Execution ---
if __name__ == "__main__":
    inv = Inventory()
    # Reading files
    inv.read_manufacturer_list('ManufacturerList.txt')
    inv.read_price_list('PriceList.txt')
    inv.read_service_dates_list('ServiceDatesList.txt')
    
    # Generating inventory reports
    inv.write_full_inventory('FullInventory.txt')
    inv.write_item_type_inventories('.')
    inv.write_past_service_date_inventory('PastServiceDateInventory.txt')
    inv.write_damaged_inventory('DamagedInventory.txt')
    
    # Start user query interface
    inv.query_inventory()
