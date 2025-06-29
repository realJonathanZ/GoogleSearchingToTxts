# This class manages file operations for saving search results to text files.

import os
from datetime import datetime
from config import RESULTS_FOLDER

class FileManager:
    def __init__(self):
        # Create results folder if it doesn't exist
        if not os.path.exists(RESULTS_FOLDER):
            os.makedirs(RESULTS_FOLDER)
    
    def save_results_to_file(self, keyword, results):
        """Save all results to a single txt file"""
        # Create filename from keyword
        safe_keyword = "".join(c for c in keyword if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_keyword = safe_keyword.replace(' ', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_keyword}_{timestamp}.txt"
        filepath = os.path.join(RESULTS_FOLDER, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(f"Search Results for: {keyword}\n")
                file.write(f"Total Results: {len(results)}\n")
                file.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write("=" * 50 + "\n\n")
                
                for i, result in enumerate(results, 1):
                    file.write(f"Name: {result['name']}\n")
                    file.write(f"Address: {result['address']}\n")
                    file.write(f"Rating: {result['rating']}\n")
                    
                    # Add empty line between results (except for last result)
                    if i < len(results):
                        file.write("\n")
            
            print(f"Results saved to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"Error saving file: {e}")
            return None
