from google_places_api import GooglePlacesAPI
from file_manager import FileManager

def main():
    print("=" * 50)
    print("Google Places Search Tool")
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
        
        try:
            # Ask user to choose search mode
            print("\nSearch Mode Options:")
            print("1. Simple search (up to 60 results, faster)")
            print("2. Enhanced search with variations (up to 150+ results, slower)")
            
            while True:
                choice = input("Choose search mode (1 or 2): ").strip()
                if choice in ['1', '2']:
                    break
                print("Please enter 1 or 2")
            
            if choice == '1':
                # Simple search mode - use original search_places method
                print("\n🔍 Simple search mode: Single search query...")
                results = places_api.search_places(keyword)
            else:
                # Enhanced search mode - use variation search
                print("\n🔍 Enhanced search mode: Using multiple search variations...")
                results = places_api.search_with_variations(keyword)
            
            if not results:
                print("No results found.")
                continue
            
            # Save results to file
            file_path = file_manager.save_results_to_file(keyword, results)
            
            if file_path:
                print(f"✓ Successfully saved {len(results)} results!")
            else:
                print("✗ Failed to save results.")
                
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
