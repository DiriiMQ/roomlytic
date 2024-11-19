import argparse
import json
import os
import shutil
from datetime import datetime

SUPPLIERS_CONFIG_FILE = "src/configs/suppliers.config.json"
BACKUP_FOLDER = "backup"

def create_backup():
    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = os.path.join(BACKUP_FOLDER, f"suppliers_{timestamp}.json")
    shutil.copy(SUPPLIERS_CONFIG_FILE, backup_file)
    print(f"Backup created at {backup_file}")

def load_suppliers():
    if not os.path.exists(SUPPLIERS_CONFIG_FILE):
        return {"suppliers": []}
    with open(SUPPLIERS_CONFIG_FILE, "r") as f:
        return json.load(f)

def save_suppliers(suppliers):
    create_backup()
    with open(SUPPLIERS_CONFIG_FILE, "w") as f:
        json.dump(suppliers, f, indent=2)

def add_supplier(file_path):
    suppliers = load_suppliers()
    with open(file_path, "r") as f:
        new_supplier = json.load(f)

    # Check if the supplier already exists
    for supplier in suppliers["suppliers"]:
        if supplier["name"] == new_supplier["name"] or supplier["url"] == new_supplier["url"]:
            print(f"Supplier with name {new_supplier['name']} or url {new_supplier['url']} already exists.")
            return

    suppliers["suppliers"].append(new_supplier)
    save_suppliers(suppliers)
    print(f"Supplier {new_supplier['name']} added successfully.")

def remove_supplier():
    suppliers = load_suppliers()
    if not suppliers["suppliers"]:
        print("No suppliers available.")
        return

    # List all suppliers with their index
    for index, supplier in enumerate(suppliers["suppliers"]):
        print(f"{index}: {supplier['name']} ({supplier['url']})")

    # Get the index to remove
    index_to_remove = int(input("Enter the index of the supplier to remove: "))
    if index_to_remove < 0 or index_to_remove >= len(suppliers["suppliers"]):
        print("Invalid index.")
        return

    removed_supplier = suppliers["suppliers"].pop(index_to_remove)
    save_suppliers(suppliers)
    print(f"Supplier {removed_supplier['name']} removed successfully.")

def main():
    parser = argparse.ArgumentParser(description="Manage suppliers.")
    parser.add_argument("--add-supplier", type=str, help="Add a new supplier from a JSON file")
    parser.add_argument("--remove-supplier", action="store_true", help="Remove an existing supplier")

    args = parser.parse_args()

    if args.add_supplier:
        add_supplier(args.add_supplier)
    elif args.remove_supplier:
        remove_supplier()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()