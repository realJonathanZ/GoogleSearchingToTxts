# Handles Google Places API calls

import requests
import time
from config import GOOGLE_PLACES_API_KEY, MAX_RESULTS

class GooglePlacesAPI:
    def __init__(self):
        self.api_key = GOOGLE_PLACES_API_KEY
        self.base_url = "https://places.googleapis.com/v1/places:searchText"
    
    def search_places(self, query):
        """Search for places using Google Places API (New) with pagination"""
        all_results = []
        next_page_token = None
        page_count = 0
        max_pages = 8  # To get up to 150 results (20 per page, need 8 pages)
        
        print(f"Searching for: {query}")
        
        while len(all_results) < MAX_RESULTS and page_count < max_pages:
            page_count += 1
            print(f"Fetching page {page_count}...")
            
            # Prepare request body for new API
            request_body = {
                "textQuery": query,
                "maxResultCount": 20  # API maximum per request
            }
            
            # Add pagination token if available
            if next_page_token:
                request_body["pageToken"] = next_page_token
            
            headers = {
                'Content-Type': 'application/json',
                'X-Goog-Api-Key': self.api_key,
                'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.rating,nextPageToken'
            }
            
            try:
                # Make API request
                response = requests.post(self.base_url, json=request_body, headers=headers)
                data = response.json()
                
                # Debug: Print response status
                print(f"HTTP Status: {response.status_code}")
                
                if response.status_code != 200:
                    print(f"API Error: {response.status_code}")
                    if 'error' in data:
                        print(f"Error details: {data['error']}")
                    break
                
                # Process results
                places = data.get('places', [])
                page_results = 0
                
                for place in places:
                    if len(all_results) >= MAX_RESULTS:
                        break
                        
                    place_info = {
                        'name': place.get('displayName', {}).get('text', 'N/A'),
                        'address': place.get('formattedAddress', 'N/A'),
                        'rating': place.get('rating', 'N/A')
                    }
                    all_results.append(place_info)
                    page_results += 1
                
                print(f"Page {page_count}: Found {page_results} results (Total: {len(all_results)})")
                
                # Check for next page token
                next_page_token = data.get('nextPageToken')
                if not next_page_token:
                    print("No more pages available")
                    break
                
                # Wait before next request (required for pagination)
                if len(all_results) < MAX_RESULTS and next_page_token:
                    print("Waiting for next page...")
                    time.sleep(2)
                    
            except Exception as e:
                print(f"Error fetching data: {e}")
                break
        
        print(f"Total results found: {len(all_results)}")
        return all_results
    
    def search_with_variations(self, base_query):
        """Search using multiple variations to get more results"""
        all_results = []
        seen_names = set()  # To avoid duplicates
        
        # Generate search variations
        variations = self.generate_search_variations(base_query)
        
        print(f"Base search: {base_query}")
        print(f"Will search {len(variations)} variations to get more results...")
        
        for i, variation in enumerate(variations, 1):
            print(f"\n--- Variation {i}/{len(variations)}: {variation} ---")
            
            # Search with this variation
            variation_results = self.search_places_single(variation)
            
            # Add unique results only
            new_results = 0
            for result in variation_results:
                # Create a unique identifier (name + address)
                unique_id = f"{result['name'].lower().strip()} | {result['address'].lower().strip()}"
                
                if unique_id not in seen_names:
                    seen_names.add(unique_id)
                    all_results.append(result)
                    new_results += 1
            
            print(f"Added {new_results} new unique results (Total unique: {len(all_results)})")
            
            # Stop if we have enough results
            if len(all_results) >= MAX_RESULTS:
                print(f"Reached target of {MAX_RESULTS} results!")
                break
            
            # Small delay between searches
            if i < len(variations):
                time.sleep(1)
        
        print(f"\n=== FINAL: Found {len(all_results)} unique results ===")
        return all_results[:MAX_RESULTS]  # Limit to MAX_RESULTS
    
    def generate_search_variations(self, base_query):
        """Generate search variations based on the base query"""
        variations = [base_query]  # Start with original
        
        # Common industry terms for textile/spinning mills
        if 'spinning' in base_query.lower() or 'mill' in base_query.lower():
            mill_terms = [
                'textile mill', 'cotton mill', 'yarn mill', 'spinning mill',
                'fabric mill', 'weaving mill', 'spinning factory', 
                'textile factory', 'cotton spinning', 'yarn manufacturing'
            ]
            
            # Extract location from original query
            location = ''
            if 'pakistan' in base_query.lower():
                location = ' Pakistan'
            elif 'karachi' in base_query.lower():
                location = ' Karachi'
            elif 'lahore' in base_query.lower():
                location = ' Lahore'
            
            # Add variations with location
            for term in mill_terms:
                variations.append(f"{term}{location}")
        
        # General business variations
        else:
            # Add plurals and related terms
            if not base_query.endswith('s'):
                variations.append(f"{base_query}s")
            
            # Add "business", "company", "shop" variations
            base_terms = [f"{base_query} business", f"{base_query} company", f"{base_query} shop"]
            variations.extend(base_terms)
        
        # Remove duplicates and return first 6 variations
        unique_variations = []
        for var in variations:
            if var not in unique_variations:
                unique_variations.append(var)
        
        return unique_variations[:6]  # Limit to 6 searches max
    
    def search_places_single(self, query):
        """Single search without variations (renamed from search_places)"""
        all_results = []
        next_page_token = None
        page_count = 0
        max_pages = 3  # Limit to 3 pages per variation (60 results max)
        
        while len(all_results) < 60 and page_count < max_pages:
            page_count += 1
            
            # Prepare request body for new API
            request_body = {
                "textQuery": query,
                "maxResultCount": 20  # API maximum per request
            }
            
            # Add pagination token if available
            if next_page_token:
                request_body["pageToken"] = next_page_token
            
            headers = {
                'Content-Type': 'application/json',
                'X-Goog-Api-Key': self.api_key,
                'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.rating,nextPageToken'
            }
            
            try:
                # Make API request
                response = requests.post(self.base_url, json=request_body, headers=headers)
                data = response.json()
                
                if response.status_code != 200:
                    break
                
                # Process results
                places = data.get('places', [])
                
                for place in places:
                    if len(all_results) >= 60:  # Limit per variation
                        break
                        
                    place_info = {
                        'name': place.get('displayName', {}).get('text', 'N/A'),
                        'address': place.get('formattedAddress', 'N/A'),
                        'rating': place.get('rating', 'N/A')
                    }
                    all_results.append(place_info)
                
                # Check for next page token
                next_page_token = data.get('nextPageToken')
                if not next_page_token:
                    break
                
                # Wait before next request (required for pagination)
                if len(all_results) < 60 and next_page_token:
                    time.sleep(2)
                    
            except Exception as e:
                break
        
        return all_results
        
    def search_places_with_location(self, query, location=None, radius_km=50):
        """Search for places with specific location bias"""
        all_results = []
        next_page_token = None
        page_count = 0
        max_pages = 8
        
        search_text = f"{query} near {location}" if location else query
        print(f"Searching for: {search_text}")
        
        while len(all_results) < MAX_RESULTS and page_count < max_pages:
            page_count += 1
            print(f"Fetching page {page_count}...")
            
            # Prepare request body
            request_body = {
                "textQuery": search_text,
                "maxResultCount": 20
            }
            
            # Add location bias if provided
            if location:
                request_body["locationBias"] = {
                    "circle": {
                        "center": {"latitude": 0, "longitude": 0},  # Would need geocoding
                        "radius": radius_km * 1000  # Convert to meters
                    }
                }
            
            if next_page_token:
                request_body["pageToken"] = next_page_token
            
            headers = {
                'Content-Type': 'application/json',
                'X-Goog-Api-Key': self.api_key,
                'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.rating,nextPageToken'
            }
            
            try:
                response = requests.post(self.base_url, json=request_body, headers=headers)
                data = response.json()
                
                if response.status_code != 200:
                    print(f"API Error: {response.status_code}")
                    if 'error' in data:
                        print(f"Error details: {data['error']}")
                    break
                
                places = data.get('places', [])
                page_results = 0
                
                for place in places:
                    if len(all_results) >= MAX_RESULTS:
                        break
                        
                    place_info = {
                        'name': place.get('displayName', {}).get('text', 'N/A'),
                        'address': place.get('formattedAddress', 'N/A'),
                        'rating': place.get('rating', 'N/A')
                    }
                    all_results.append(place_info)
                    page_results += 1
                
                print(f"Page {page_count}: Found {page_results} results (Total: {len(all_results)})")
                
                next_page_token = data.get('nextPageToken')
                if not next_page_token:
                    print("No more pages available")
                    break
                
                if len(all_results) < MAX_RESULTS and next_page_token:
                    print("Waiting for next page...")
                    time.sleep(2)
                    
            except Exception as e:
                print(f"Error fetching data: {e}")
                break
        
        return all_results

    # ...existing code...
