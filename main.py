import argparse
import json
from src.cli.hotel_data_cli import HotelDataCLI

def main():
    parser = argparse.ArgumentParser(description="Process hotel and destination IDs.")
    parser.add_argument("hotel_ids", type=str, help="Comma-separated list of hotel IDs")
    parser.add_argument("destination_ids", type=str, help="Comma-separated list of destination IDs")
    
    args = parser.parse_args()
    
    hotel_ids = args.hotel_ids.split(",")
    destination_ids = args.destination_ids.split(",")
    
    cli = HotelDataCLI()
    hotels = cli.convert_list_hotel_2_list_dict(cli.run(hotel_ids, destination_ids))

    print(json.dumps(hotels, indent=2))

if __name__ == "__main__":
    main()