import pandas as pd
import requests
import time
from tqdm import tqdm
import os

# Configuration
API_KEY = 'YOUR-API-KEY-HERE'  # Replace with your actual API key
INPUT_FILE = 'YOUR_INPUT_FILE.csv'  # Replace with your input CSV file path
OUTPUT_FILE = 'YOUR_OUTPUT_FILE.csv'  # Replace with your desired output CSV file path

# Check if output file exists (resume mode)
if os.path.exists(OUTPUT_FILE):
    print("Found existing output file. Resuming from where we left off...")
    df = pd.read_csv(OUTPUT_FILE)
    resume_mode = True
else:
    print("Starting fresh - reading input CSV file...")
    df = pd.read_csv(INPUT_FILE)
    # Create new columns for location data
    df['Country'] = ''
    df['Country Code'] = ''
    df['City'] = ''
    df['State'] = ''
    df['Latitude'] = ''
    df['Longitude'] = ''
    resume_mode = False


# Function to get IP location
def get_ip_location(ip):
    url = f'https://api.ipgeolocation.io/ipgeo?apiKey={API_KEY}&ip={ip}'
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            return {
                'country': data.get('country_name', ''),
                'country_code': data.get('country_code2', ''),
                'city': data.get('city', ''),
                'state': data.get('state_prov', ''),
                'latitude': data.get('latitude', ''),
                'longitude': data.get('longitude', '')
            }
        else:
            print(f"\nError for IP {ip}: Status {response.status_code}")
            return None
    except requests.exceptions.Timeout:
        print(f"\nTimeout for IP {ip} - will retry later")
        return None
    except Exception as e:
        print(f"\nError for IP {ip}: {str(e)}")
        return None


# Count IPs that need processing (where Country is empty/null)
ips_to_process = df[df['Country'].isna() | (df['Country'] == '')].index.tolist()
total_to_process = len(ips_to_process)
already_processed = len(df) - total_to_process

print(f"\nTotal IPs: {len(df)}")
print(f"Already processed: {already_processed}")
print(f"Need to process: {total_to_process}")
print(f"Starting processing...\n")

if total_to_process == 0:
    print("All IPs have been processed!")
else:
    processed_count = 0
    api_calls_made = 0

    # Process only IPs with missing data
    for idx in tqdm(ips_to_process, desc="Processing IPs"):
        ip = df.at[idx, 'Ip Address']

        if pd.isna(ip) or ip == '':
            continue

        location = get_ip_location(ip)
        api_calls_made += 1

        if location:
            df.at[idx, 'Country'] = location['country']
            df.at[idx, 'Country Code'] = location['country_code']
            df.at[idx, 'City'] = location['city']
            df.at[idx, 'State'] = location['state']
            df.at[idx, 'Latitude'] = location['latitude']
            df.at[idx, 'Longitude'] = location['longitude']
            processed_count += 1

        # Rate limiting: free tier allows ~1 request per second
        time.sleep(1.1)

        # Save progress every 50 IPs
        if api_calls_made % 50 == 0:
            df.to_csv(OUTPUT_FILE, index=False)
            remaining = total_to_process - processed_count
            print(f"\nProgress saved: {processed_count}/{total_to_process} IPs processed")
            print(f"API calls made in this session: {api_calls_made}")
            print(f"Remaining: {remaining}")

    # Save final results
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\n{'=' * 60}")
    print(f"Session Complete!")
    print(f"{'=' * 60}")
    print(f"Successfully processed: {processed_count} IPs")
    print(f"API calls made in this session: {api_calls_made}")
    print(f"Results saved to: {OUTPUT_FILE}")

    # Check if there are still missing entries
    still_missing = len(df[df['Country'].isna() | (df['Country'] == '')])
    if still_missing > 0:
        print(f"\nNote: {still_missing} IPs still need processing (likely due to timeouts)")
        print("Run the script again to retry those IPs.")
    else:
        print("\nAll IPs successfully processed!")