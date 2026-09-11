# Phone Number Metadata Viewer & Geocoder

A Python script that parses a phone number to extract its basic metadata (carrier and broad location text) and plots the region's geographic center onto an interactive map.

This project serves as an educational tool to demonstrate how phone numbers store static registration data (like a country or state), rather than broadcasting real-time device locations.

## 🚀 Features

- **Metadata Extraction:** Reads user input to extract the phone number's original service provider and regional description.
- **Geocoding:** Passes the extracted regional text string to the OpenCage API to find its latitude and longitude.
- **Map Generation:** Uses Folium to generate an interactive HTML map pinpointing the center of that region.

## 🛠️ Requirements & Dependencies

The project relies on the following Python packages:

- `phonenumbers` - To parse the phone number metadata and carrier info.
- `opencage` - To turn the text location into coordinates.
- `folium` - To build and render the interactive map.
- `python-dotenv` - To securely load your API credentials.

## 📋 Prerequisites

You need a free API key from OpenCage to fetch the map coordinates.
1. Sign up for an account at [OpenCage Data](https://opencagedata.com).
2. Get your API key from the dashboard.

## 🔧 Setup & Installation

1. **Install the dependencies:**
   ```bash
   pip install phonenumbers opencage folium python-dotenv
   ```

2. **Configure your Environment Variables:**
   Create a `.env` file in the root directory of your project and add your API key:
   ```env
   OPENCAGE_API_KEY=your_opencage_api_key_here
   ```

## 💻 How It Works

Run the script from your terminal:
```bash
python main.py
```

1. Enter a full phone number including the country code (e.g., `+14155552671`).
2. The script prints the parsed **Location Text** and the **Service Provider**.
3. It passes that broad location text to the OpenCage Geocoder.
4. The coordinates are calculated, and a `phone_number_location.html` file is generated inside an `output/` directory two levels above the script.

## 📌 Technical Note on Accuracy

If the pin on your generated map feels incorrect or generalized, **the script is working exactly as intended**. 

The `phonenumbers` library can only read embedded metadata from a phone digits string (such as country or area codes). When it extracts a text description like `"California"` or `"United Kingdom"`, the OpenCage Geocoder has no choice but to return the **exact mathematical center point (centroid) of that entire territory**. Individual phone numbers do not publicly expose live GPS positions or tower data.
