#!/usr/bin/env python3
"""Simple test using urllib to test the API endpoint."""

import urllib.request
import urllib.parse
import json
from datetime import datetime, timedelta


def test_api_with_params(params, test_name):
    """Test the Canal & River Trust API endpoint with specific parameters."""
    url = "https://canalrivertrust.org.uk/api/stoppage/notices"

    # Build the full URL
    query_string = urllib.parse.urlencode(params)
    full_url = f"{url}?{query_string}"

    print(f"\n=== {test_name} ===")
    print(f"Testing URL: {full_url}")

    # Create request with browser-like headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
    }

    req = urllib.request.Request(full_url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            status = response.getcode()
            content_type = response.headers.get('content-type', 'Unknown')

            print(f"Status: {status}")
            print(f"Content-Type: {content_type}")

            data = response.read().decode('utf-8')

            if status == 200:
                if 'json' in content_type.lower():
                    try:
                        json_data = json.loads(data)
                        print(f"JSON response received")
                        print(f"Features found: {len(json_data.get('features', []))}")

                        if json_data.get('features'):
                            first_feature = json_data['features'][0]
                            print(f"Sample feature keys: {list(first_feature.keys())}")
                            if 'properties' in first_feature:
                                print(f"Sample properties: {list(first_feature['properties'].keys())}")
                                print(f"Sample title: {first_feature['properties'].get('title', 'N/A')}")
                    except json.JSONDecodeError as e:
                        print(f"Failed to parse JSON: {e}")
                        print(f"Response (first 500 chars): {data[:500]}")
                else:
                    print(f"Non-JSON response received (first 500 chars):")
                    print(data[:500])

                    # Check if it's the "Service Unavailable" HTML page
                    if 'service unavailable' in data.lower():
                        print("\n*** API is returning 'Service Unavailable' page ***")
                        print("This matches the error seen in Home Assistant logs")
            else:
                print(f"HTTP Error: {status}")
                print(f"Response content (first 500 chars): {data[:500]}")

    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        try:
            error_data = e.read().decode('utf-8')
            print(f"Error response (first 500 chars): {error_data[:500]}")

            # Check if it's the "Service Unavailable" HTML page
            if 'service unavailable' in error_data.lower():
                print("\n*** API is returning 'Service Unavailable' page ***")
                print("This matches the error seen in Home Assistant logs")
        except:
            print("Could not read error response")
    except Exception as e:
        print(f"Exception: {e}")


def test_api():
    """Run multiple API tests with different parameters."""

    # Test 1: Current integration parameters (fixed)
    params1 = {
        "consult": "false",
        "geometry": "point",
        "start": datetime.now().strftime("%Y-%m-%d"),
        "end": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
        "fields": "title,region,waterways,path,typeId,reasonId,programmeId,start,end,state"
    }
    test_api_with_params(params1, "Current Integration Parameters")

    # Test 2: Minimal parameters
    params2 = {
        "consult": "false",
        "start": datetime.now().strftime("%Y-%m-%d"),
        "end": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    }
    test_api_with_params(params2, "Minimal Parameters")

    # Test 3: No parameters (see what default gives us)
    params3 = {}
    test_api_with_params(params3, "No Parameters")

    # Test 4: Exact Postman parameter order
    params4 = {
        "consult": "false",
        "geometry": "point",
        "start": "2025-07-07",
        "end": "2025-07-20",
        "fields": "title,region,waterways,path,typeId,reasonId,programmeId,start,end,state"
    }
    test_api_with_params(params4, "Exact Postman Parameter Order")


if __name__ == "__main__":
    print("Canal & River Trust API Simple Test")
    print(f"Test run at: {datetime.now()}")
    test_api()
