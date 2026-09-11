import os
import sys
from pathlib import Path

import folium
import phonenumbers
from dotenv import load_dotenv
from opencage.geocoder import OpenCageGeocode
from phonenumbers import carrier
from phonenumbers import geocoder as phone_geocoder  # Renamed to avoid conflicts

# 1. Gather User Input
my_number = input("Enter a phone number (with country code, e.g., +14155552671): ")

try:
    pepnumber = phonenumbers.parse(my_number)
except Exception as e:  # noqa: BLE001
    print(f"Error parsing number: {e}")
    sys.exit()

# 2. Extract Static Metadata
location_text = phone_geocoder.description_for_number(pepnumber, "en")
provider_text = carrier.name_for_number(pepnumber, "en")

print(f"The metadata location is: {location_text}")
print(f"The original service provider is: {provider_text}")

if not location_text:
    print("Could not extract a meaningful location string from this phone number.")
    sys.exit()

# 3. Initialize OpenCage API Safely
load_dotenv()
api_key = os.environ.get("OPENCAGE_API_KEY")
if not api_key:
    print("Error: OPENCAGE_API_KEY not found in your environment/.env file.")
    sys.exit()

opencage_client = OpenCageGeocode(api_key)
results = opencage_client.geocode(str(location_text))

# 4. Check if Geocoding Returned Any Results Safely
if results and len(results) > 0:
    lat = results[0]["geometry"]["lat"]
    lng = results[0]["geometry"]["lng"]

    # 5. Build Map
    my_map = folium.Map(
        location=[lat, lng], zoom_start=6
    )  # Lowered zoom since it's a broad area
    folium.Marker([lat, lng], popup=location_text).add_to(my_map)

    # 6. Safe File Saving System
    THIS_FILE = Path(__file__).resolve()
    PROJECT_ROOT = THIS_FILE.parents[2]
    output_dir = PROJECT_ROOT / "output"

    # Create the directory automatically if it doesn't exist yet
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "phone_number_location.html"
    my_map.save(output_path)
    print(f"Success! Map saved safely to: {output_path}")
else:
    print(f"OpenCage could not find coordinates for the text: '{location_text}'")
