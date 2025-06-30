# Handles Google Places API calls

import requests
import time
from config import GOOGLE_PLACES_API_KEY, MAX_RESULTS
from variation_determination import VariationDetermination

class GooglePlacesAPI:
    def __init__(self):
        self.api_key = GOOGLE_PLACES_API_KEY
        self.base_url = "https://places.googleapis.com/v1/places:searchText"
        self.variation_generator = VariationDetermination()
    
    # tested!
    def search_places(self, query, max_pages=8, max_results=None, verbose=True):
        """Search for places using Google Places API (New) with pagination
        
        Args:
            query (str): The search query for places.
            max_pages (int): Maximum number of pages to fetch. Defaults to 8.
            max_results (int): Maximum number of results to return. Defaults to MAX_RESULTS.
            verbose (bool): If True, print detailed output. Defaults to True.

        Note:
            verbose is automatically set to False when searching with variations.
            
        Status: Tested and working
        """
        if max_results is None:
            max_results = MAX_RESULTS
            
        all_results = []
        next_page_token = None
        page_count = 0
        
        if verbose:
            print(f"Searching for: {query}")
        
        while len(all_results) < max_results and page_count < max_pages:
            page_count += 1
            if verbose:
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
                if verbose:
                    print(f"HTTP Status: {response.status_code}")
                
                if response.status_code != 200:
                    if verbose:
                        print(f"API Error: {response.status_code}")
                        if 'error' in data:
                            print(f"Error details: {data['error']}")
                    break
                
                # Process results
                places = data.get('places', [])
                page_results = 0
                
                for place in places:
                    if len(all_results) >= max_results:
                        break
                        
                    place_info = {
                        'name': place.get('displayName', {}).get('text', 'N/A'),
                        'address': place.get('formattedAddress', 'N/A'),
                        'rating': place.get('rating', 'N/A')
                    }
                    all_results.append(place_info)
                    page_results += 1
                
                if verbose:
                    print(f"Page {page_count}: Found {page_results} results (Total: {len(all_results)})")
                
                # Check for next page token
                next_page_token = data.get('nextPageToken')
                if not next_page_token:
                    if verbose:
                        print("No more pages available")
                    break
                
                # Wait before next request (required for pagination)
                if len(all_results) < max_results and next_page_token:
                    if verbose:
                        print("Waiting for next page...")
                    time.sleep(2)
                    
            except Exception as e:
                if verbose:
                    print(f"Error fetching data: {e}")
                break
        
        if verbose:
            print(f"Total results found: {len(all_results)}")
        return all_results
    
    # tested!
    def search_with_variations(self, base_query):
        """Search using multiple variations to get more results
        
        Status: Tested and working
        """
        all_results = []
        seen_names = set()  # To avoid duplicates
        
        # Generate search variations using the variation determination module
        variations = self.variation_generator.generate_search_variations(base_query)
        
        print(f"Base search: {base_query}")
        print(f"Will search {len(variations)} variations to get more results...")
        
        for i, variation in enumerate(variations, 1):
            print(f"\n--- Variation {i}/{len(variations)}: {variation} ---")
            
            # Search with this variation using the main search method (limited pages, no verbose output)
            variation_results = self.search_places(variation, max_pages=3, max_results=60, verbose=False)
            
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


    # not tested and not used yet
    def search_places_with_location(self, query, location=None, radius_km=50):
        """Search for places with specific location bias
        
        Note: This method is not tested and was adapted from another open source project.
              Location bias implementation may need geocoding service integration.
        """
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

