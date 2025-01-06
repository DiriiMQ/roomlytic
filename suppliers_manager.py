import argparse
import json
import os
import shutil
from datetime import datetime
from src.config_generation.config_generator import ConfigGenerator
from src.config_generation.default_generation_strategy import DefaultGenerationStrategy
from src.config_generation.openai_generation_strategy import OpenAIGenerationStrategy

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

def generate_config(supplier_info, is_openai=False):
    if is_openai:
        strategy = OpenAIGenerationStrategy()
    else:
        strategy = DefaultGenerationStrategy()

    config = strategy.generate_config(supplier_info)
    return config

def main():
    parser = argparse.ArgumentParser(description="Manage suppliers.")
    parser.add_argument("--add-supplier", type=str, help="Add a new supplier from a JSON file")
    parser.add_argument("--remove-supplier", action="store_true", help="Remove an existing supplier")
    
    # add --generate-config argument to input supplier name, and url and set llm to true or false then call generate_config function
    # add --openai argument to call generate_config function with is_openai=True
    # add --llm argument to call generate_config function with is_openai=False

    parser.add_argument("--generate-config", type=str, help="Generate config for a supplier")
    parser.add_argument("--openai", action="store_true", help="Generate config using OpenAI")
    parser.add_argument("--llm", action="store_true", help="Generate config using LLM")

    args = parser.parse_args()

    if args.add_supplier:
        add_supplier(args.add_supplier)
    elif args.remove_supplier:
        remove_supplier()
    elif args.generate_config:
        supplier_info = {
            "name": args.generate_config,
            "url": input("Enter the URL of the supplier: ")
        }
        config = generate_config(supplier_info, is_openai=args.openai)
        supplier_info["config"] = config
        print(json.dumps(supplier_info, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()