# IP Geolocation Lookup Tool

Python script to bulk lookup IP addresses and get their geographic locations using ipgeolocation.io API.

## Features

- Processes CSV files with IP addresses
- Smart resume capability (skips already processed IPs)
- Progress saving every 50 IPs
- Handles timeouts and errors gracefully

## Setup

### 1. Create virtual environment

```bash
python3 -m venv ip_lookup_env
source ip_lookup_env/bin/activate
```

### 2. Install dependencies

```bash
pip install pandas requests tqdm
```

### 3. Add your API key

Update the `API_KEY` variable in `ip_lookup.py`:

```python
API_KEY = 'your_api_key_here'
```

### 4. Run the script

```bash
python ip_lookup.py
```

## Requirements

- Python 3.x
- pandas
- requests
- tqdm

## Usage

1. Place your CSV file with IP addresses in the same folder
2. Update `INPUT_FILE` variable in the script to match your CSV filename
3. Run the script - it will create/update `ip_locations.csv`
4. Re-run anytime to process remaining IPs (only processes missing entries)

## Output

The script creates `ip_locations.csv` with the following columns:

- Ip Address
- Country
- Country Code
- City
- State
- Latitude
- Longitude

## API Information

This tool uses ipgeolocation.io API:

- Free tier: 1000 requests/day
- Rate limit: ~1 request per second
- Sign up at: https://ipgeolocation.io

## Notes

- The script automatically resumes from where it left off
- Progress is saved every 50 IP lookups
- Timeouts are handled gracefully and can be retried by running the script again
- CSV files and virtual environment are excluded from version control