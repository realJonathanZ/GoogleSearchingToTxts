from google_places_api import GooglePlacesAPI
from file_manager import FileManager

def main():
    print("=" * 50)
    print("Google Places Search Tool - Enhanced")
    print("=" * 50)
    
    # Initialize components
    places_api = GooglePlacesAPI()
    file_manager = FileManager()
    
    while True:
        # Get keyword from user
        keyword = input("\nEnter search keyword (or 'quit' to exit): ").strip()
        
        if keyword.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not keyword:
            print("Please enter a valid keyword.")
            continue
        
        # Ask user if they want enhanced search
        enhanced = input("Use enhanced search for more results? (y/n): ").strip().lower()
        
        try:
            all_results = []
            seen_names = set()  # To avoid duplicates
            
            if enhanced == 'y':
                # Create search variations
                search_queries = generate_search_variations(keyword)
                print(f"Running {len(search_queries)} enhanced searches...")
                
                for i, query in enumerate(search_queries, 1):
                    print(f"\n--- Search {i}/{len(search_queries)}: '{query}' ---")
                    results = places_api.search_places(query)
                    
                    # Add unique results
                    for result in results:
                        name_key = result['name'].lower().strip()
                        if name_key not in seen_names:
                            seen_names.add(name_key)
                            all_results.append(result)
                    
                    print(f"Total unique results so far: {len(all_results)}")
            else:
                # Single search
                all_results = places_api.search_places(keyword)
            
            if not all_results:
                print("No results found.")
                continue
            
            # Save results to file
            file_path = file_manager.save_results_to_file(keyword, all_results)
            
            if file_path:
                print(f"✓ Successfully saved {len(all_results)} unique results!")
            else:
                print("✗ Failed to save results.")
                
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
        except Exception as e:
            print(f"An error occurred: {e}")

def generate_search_variations(keyword):
    """Generate multiple search variations to get more results"""
    base_variations = [
        keyword,
        f"{keyword} company",
        f"{keyword} business",
        f"{keyword} factory",
        f"{keyword} industry",
        f"{keyword} manufacturing"
    ]
    
    # Add location-specific variations for Pakistan
    if "pakistan" in keyword.lower():
        base_keyword = keyword.replace("Pakistan", "").replace("pakistan", "").strip()
        location_variations = [
            f"{base_keyword} Karachi",
            f"{base_keyword} Lahore", 
            f"{base_keyword} Faisalabad",
            f"{base_keyword} Rawalpindi",
            f"{base_keyword} Multan",
            f"{base_keyword} Peshawar"
        ]
        base_variations.extend(location_variations)
    
    return base_variations

if __name__ == "__main__":
    main()
