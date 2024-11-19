import os
from twilio.rest import Client
import requests

# Twilio API Credentials
ACCOUNT_SID = "AC3e59540a700c3bc49e621ee2s3f9x0g4d8"
AUTH_TOKEN = "79d19eba6b7b33f7f9w0v9e2j0g"
TWILIO_PHONE_LOOKUP_URL = "https://lookups.twilio.com/v1/PhoneNumbers/"

# Geolocation API (dummy example, replace with an actual API)
GEOLOCATION_API_URL = "https://api.ipstack.com/"
GEOLOCATION_API_KEY = "ec107937f0ee1216ed8c20dbad250020"

# Initialize Twilio Client
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Mock contact database
CONTACTS_DATABASE = {
    "+1234567890": {"Name": "John Doe", "Email": "john.doe@example.com", "Address": "123 Elm Street"},
    "+1987654321": {"Name": "Jane Smith", "Email": "jane.smith@example.com", "Address": "456 Oak Avenue"},
}

def lookup_phone_number(phone_number):
    """
    Lookup phone number using Twilio API.
    """
    try:
        response = client.lookups.phone_numbers(phone_number).fetch(type=["carrier"])
        carrier_info = {
            "Phone Number": response.phone_number,
            "Country Code": response.country_code,
            "Carrier": response.carrier.get("name", "Unknown"),
            "Type": response.carrier.get("type", "Unknown"),
        }
        return carrier_info
    except Exception as e:
        return {"Error": str(e)}

def geolocate_number(phone_number):
    """
    Dummy geolocation function, replace with actual API logic.
    """
    try:
        # For real use, you'd extract country code or use a phone-to-location API
        response = requests.get(
            f"{GEOLOCATION_API_URL}/{phone_number}?access_key={GEOLOCATION_API_KEY}"
        )
        if response.status_code == 200:
            data = response.json()
            return {
                "Continent": data.get("continent_name"),
                "Country": data.get("country_name"),
                "Region": data.get("region_name"),
                "City": data.get("city"),
            }
        else:
            return {"Error": "Failed to retrieve geolocation data"}
    except Exception as e:
        return {"Error": str(e)}

def fetch_contact_details(phone_number):
    """
    Fetch contact details from a mock local database.
    """
    return CONTACTS_DATABASE.get(phone_number, {"Error": "Contact not found in database."})

def main():
    print("Global Phone Number Tracker")
    phone_number = input("Enter the phone number with country code (e.g., +1234567890): ")

    print("\nLooking up phone number...")
    phone_info = lookup_phone_number(phone_number)
    if "Error" in phone_info:
        print(phone_info["Error"])
        return

    print("\nPhone Information:")
    for key, value in phone_info.items():
        print(f"{key}: {value}")

    print("\nFetching contact details...")
    contact_details = fetch_contact_details(phone_number)
    if "Error" in contact_details:
        print(contact_details["Error"])
    else:
        print("\nContact Details:")
        for key, value in contact_details.items():
            print(f"{key}: {value}")

    print("\nFetching geolocation...")
    location_info = geolocate_number(phone_number)
    if "Error" in location_info:
        print(location_info["Error"])
    else:
        print("\nGeolocation Information:")
        for key, value in location_info.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()
