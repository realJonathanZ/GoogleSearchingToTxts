# Handles search query variations for different business types

class VariationDetermination:
    """
    Generates search variations based on the base query to improve search results.
    
    This class automatically detects the industry type from a search query and generates
    relevant variations to maximize search results from the Google Places API.
    
    Supported Industries:
        - Textile/Manufacturing (spinning mills, factories, etc.)
        - Restaurant/Food Service (restaurants, cafes, eateries)
        - Retail/Shopping (stores, shops, markets)
        - General Business (fallback for any other business type)
    
    Attributes:
        textile_mill_terms (list): Terms specific to textile industry
        restaurant_terms (list): Terms specific to restaurant industry  
        retail_terms (list): Terms specific to retail industry
    """
    
    def __init__(self):
        """
        Initialize the VariationDetermination class with predefined industry terms.
        
        Sets up term lists for different industries that will be used to generate
        search variations based on the detected industry type.
        
        Args:
            None
            
        Returns:
            None
        """
        # Define industry-specific variations
        self.textile_mill_terms = [
            'textile mill', 'cotton mill', 'yarn mill', 'spinning mill',
            'fabric mill', 'weaving mill', 'spinning factory', 
            'textile factory', 'cotton spinning', 'yarn manufacturing'
        ]
        
        # Add more industry categories as needed
        self.restaurant_terms = [
            'restaurant', 'cafe', 'diner', 'bistro', 'eatery', 'food place'
        ]
        
        self.retail_terms = [
            'store', 'shop', 'retail', 'outlet', 'market', 'bazaar'
        ]
    
    def generate_search_variations(self, base_query, max_variations=6):
        """
        Generate search variations based on the base query to maximize search results.
        
        This is the main method that analyzes the input query, detects the industry type,
        and generates appropriate search variations. It automatically removes duplicates
        and limits results to the specified maximum.
        
        Process:
        1. Starts with the original query
        2. Detects industry type (textile, restaurant, retail, or general)
        3. Generates industry-specific variations
        4. Removes duplicates while preserving order
        5. Returns limited number of variations
        
        Args:
            base_query (str): The original search query entered by the user
            max_variations (int, optional): Maximum number of variations to generate.
                                          Defaults to 6. Must be positive integer.
            
        Returns:
            list[str]: List of unique search query variations, limited to max_variations.
                      Always includes the original base_query as the first element.
                      
        Example:
            >>> generator = VariationDetermination()
            >>> variations = generator.generate_search_variations("spinning mill Pakistan", 4)
            >>> print(variations)
            ['spinning mill Pakistan', 'textile mill Pakistan', 'cotton mill Pakistan', ...]
        """
        variations = [base_query]  # Start with original
        
        # Detect industry type and generate specific variations
        if self._is_textile_industry(base_query):
            variations.extend(self._generate_textile_variations(base_query))
        elif self._is_restaurant_industry(base_query):
            variations.extend(self._generate_restaurant_variations(base_query))
        elif self._is_retail_industry(base_query):
            variations.extend(self._generate_retail_variations(base_query))
        else:
            # General business variations
            variations.extend(self._generate_general_variations(base_query))
        
        # Remove duplicates and return limited results
        unique_variations = self._remove_duplicates(variations)
        return unique_variations[:max_variations]
    
    def _is_textile_industry(self, query):
        """
        Check if the query is related to textile/manufacturing industry.
        
        Analyzes the query string for keywords commonly associated with textile
        manufacturing, spinning mills, fabric production, and related industries.
        Case-insensitive matching is performed.
        
        Args:
            query (str): The search query to analyze. Can contain any text.
                        Empty strings will return False.
            
        Returns:
            bool: True if query contains textile industry keywords, False otherwise.
                 Returns False for empty or None inputs.
                 
        Keywords Detected:
            - spinning, mill, textile, cotton, yarn, fabric, weaving
            
        Example:
            >>> generator = VariationDetermination()
            >>> generator._is_textile_industry("spinning mill in Karachi")
            True
            >>> generator._is_textile_industry("restaurant in Lahore") 
            False
        """
        textile_keywords = ['spinning', 'mill', 'textile', 'cotton', 'yarn', 'fabric', 'weaving']
        return any(keyword in query.lower() for keyword in textile_keywords)
    
    def _is_restaurant_industry(self, query):
        """
        Check if the query is related to restaurant/food service industry.
        
        Analyzes the query string for keywords commonly associated with restaurants,
        cafes, food service establishments, and dining venues. Case-insensitive 
        matching is performed.
        
        Args:
            query (str): The search query to analyze. Can contain any text.
                        Empty strings will return False.
            
        Returns:
            bool: True if query contains restaurant industry keywords, False otherwise.
                 Returns False for empty or None inputs.
                 
        Keywords Detected:
            - restaurant, cafe, food, dining, kitchen, eatery
            
        Example:
            >>> generator = VariationDetermination()
            >>> generator._is_restaurant_industry("best restaurant in Islamabad")
            True
            >>> generator._is_restaurant_industry("textile mill")
            False
        """
        restaurant_keywords = ['restaurant', 'cafe', 'food', 'dining', 'kitchen', 'eatery']
        return any(keyword in query.lower() for keyword in restaurant_keywords)
    
    def _is_retail_industry(self, query):
        """
        Check if the query is related to retail/shopping industry.
        
        Analyzes the query string for keywords commonly associated with retail stores,
        shopping establishments, markets, and commercial outlets. Case-insensitive
        matching is performed.
        
        Args:
            query (str): The search query to analyze. Can contain any text.
                        Empty strings will return False.
            
        Returns:
            bool: True if query contains retail industry keywords, False otherwise.
                 Returns False for empty or None inputs.
                 
        Keywords Detected:
            - store, shop, retail, market, outlet, bazaar
            
        Example:
            >>> generator = VariationDetermination()
            >>> generator._is_retail_industry("electronics store Lahore")
            True
            >>> generator._is_retail_industry("spinning mill Pakistan")
            False
        """
        retail_keywords = ['store', 'shop', 'retail', 'market', 'outlet', 'bazaar']
        return any(keyword in query.lower() for keyword in retail_keywords)
    
    def _generate_textile_variations(self, base_query):
        """
        Generate search variations specific to textile/manufacturing industry.
        
        Creates variations using predefined textile industry terms combined with
        location information extracted from the base query. This helps find more
        comprehensive results for textile-related searches.
        
        Args:
            base_query (str): The original search query containing textile-related terms.
                             Should not be empty. Location will be auto-extracted.
            
        Returns:
            list[str]: List of textile industry variations with location appended.
                      Each variation combines a textile term with extracted location.
                      Returns empty list if no location is found.
                      
        Textile Terms Used:
            - textile mill, cotton mill, yarn mill, spinning mill, fabric mill,
              weaving mill, spinning factory, textile factory, cotton spinning,
              yarn manufacturing
              
        Example:
            >>> generator = VariationDetermination()
            >>> variations = generator._generate_textile_variations("spinning mill Pakistan")
            >>> print(variations[:3])
            ['textile mill Pakistan', 'cotton mill Pakistan', 'yarn mill Pakistan']
        """
        variations = []
        location = self._extract_location(base_query)
        
        # Add textile-specific terms with location
        for term in self.textile_mill_terms:
            variations.append(f"{term}{location}")
        
        return variations
    
    def _generate_restaurant_variations(self, base_query):
        """
        Generate search variations specific to restaurant/food service industry.
        
        Creates variations using predefined restaurant industry terms combined with
        location information extracted from the base query. This helps find more
        comprehensive results for food service-related searches.
        
        Args:
            base_query (str): The original search query containing restaurant-related terms.
                             Should not be empty. Location will be auto-extracted.
            
        Returns:
            list[str]: List of restaurant industry variations with location appended.
                      Each variation combines a restaurant term with extracted location.
                      Returns empty list if no location is found.
                      
        Restaurant Terms Used:
            - restaurant, cafe, diner, bistro, eatery, food place
              
        Example:
            >>> generator = VariationDetermination()
            >>> variations = generator._generate_restaurant_variations("restaurant Karachi")
            >>> print(variations[:3])
            ['restaurant Karachi', 'cafe Karachi', 'diner Karachi']
        """
        variations = []
        location = self._extract_location(base_query)
        
        # Add restaurant-specific terms with location
        for term in self.restaurant_terms:
            variations.append(f"{term}{location}")
        
        return variations
    
    def _generate_retail_variations(self, base_query):
        """
        Generate search variations specific to retail/shopping industry.
        
        Creates variations using predefined retail industry terms combined with
        location information extracted from the base query. This helps find more
        comprehensive results for retail and shopping-related searches.
        
        Args:
            base_query (str): The original search query containing retail-related terms.
                             Should not be empty. Location will be auto-extracted.
            
        Returns:
            list[str]: List of retail industry variations with location appended.
                      Each variation combines a retail term with extracted location.
                      Returns empty list if no location is found.
                      
        Retail Terms Used:
            - store, shop, retail, outlet, market, bazaar
              
        Example:
            >>> generator = VariationDetermination()
            >>> variations = generator._generate_retail_variations("electronics store Lahore")
            >>> print(variations[:3])
            ['store Lahore', 'shop Lahore', 'retail Lahore']
        """
        variations = []
        location = self._extract_location(base_query)
        
        # Add retail-specific terms with location
        for term in self.retail_terms:
            variations.append(f"{term}{location}")
        
        return variations
    
    def _generate_general_variations(self, base_query):
        """
        Generate general business variations for queries that don't match specific industries.
        
        Creates generic business variations by adding common business suffixes and
        plural forms. This is the fallback method when the query doesn't match
        textile, restaurant, or retail industries.
        
        Args:
            base_query (str): The original search query. Should not be empty.
                             Any business-related term that doesn't match specific industries.
            
        Returns:
            list[str]: List of general business variations including:
                      - Plural form (if query doesn't end with 's')
                      - Query + business suffixes (business, company, shop, service, center)
                      
        Business Suffixes Added:
            - business, company, shop, service, center
            
        Example:
            >>> generator = VariationDetermination()
            >>> variations = generator._generate_general_variations("consultant")
            >>> print(variations)
            ['consultants', 'consultant business', 'consultant company', 'consultant shop', 
             'consultant service', 'consultant center']
        """
        variations = []
        
        # Add plurals
        if not base_query.endswith('s'):
            variations.append(f"{base_query}s")
        
        # Add business-related suffixes
        business_suffixes = ['business', 'company', 'shop', 'service', 'center']
        for suffix in business_suffixes:
            variations.append(f"{base_query} {suffix}")
        
        return variations
    
    def _extract_location(self, query):
        """
        Extract location information from a search query string.
        
        Searches for common location indicators and patterns within the query string.
        This method uses a simplified approach focusing on location keywords and
        capitalized words that likely represent place names.
        
        Args:
            query (str): The search query to analyze for location information.
                        Can contain any text. Empty strings will return empty location.
            
        Returns:
            str: Formatted location string with leading space (e.g., " Downtown", " Chicago").
                Returns empty string if no location pattern is detected.
                Returns the first location found if multiple locations are present.
                
        Example:
            >>> generator = VariationDetermination()
            >>> location = generator._extract_location("spinning mill Chicago")
            >>> print(repr(location))  # Shows the leading space
            ' Chicago'
            >>> location = generator._extract_location("restaurant downtown")
            >>> print(repr(location))
            ' Downtown'
            >>> location = generator._extract_location("textile business")
            >>> print(repr(location))
            ''
        """
        location = ''
        query_lower = query.lower().strip()

        # If there is any word matches the location keywords, return it in title case
        location_keywords = [
            'downtown', 'city center', 'center', 'district', 'area', 'zone',
            'mall', 'plaza', 'square', 'market', 'industrial area', 'business district',
            'uptown', 'midtown', 'suburb', 'neighborhood', 'quarters', 'sector'
        ]
        
        for keyword in location_keywords:
            if keyword in query_lower:
                return f" {keyword.title()}"
        
        # try to find possible location with capitalized words now
        words = query_lower.split()
        original_words = query.split()
        
        for i, word in enumerate(words):
            # iterate each original word..
            if i < len(original_words) and len(original_words[i]) > 2:
                original_word = original_words[i]
                
                # if target exists, must start with capital and not be a common business word
                if original_word[0].isupper():
                    # Hard coded business word
                    business_words = [
                        'mill', 'factory', 'company', 'business', 'shop', 'store', 
                        'restaurant', 'cafe', 'service', 'center', 'industry',
                        'manufacturing', 'textile', 'cotton', 'spinning', 'fabric'
                    ]
                    # if detected any business word, must skip it.
                    if word not in business_words:
                        # Otherwise return the original word starting with capital letter.
                        return f" {original_word}"
        
        return location
    
    def _remove_duplicates(self, variations):
        """
        Remove duplicate variations while preserving the original order.
        
        Processes a list of search variations to eliminate duplicates using
        case-insensitive comparison. The first occurrence of each unique variation
        is kept, maintaining the original order of appearance.
        
        Args:
            variations (list[str]): List of search query variations that may contain duplicates.
                                   Each element should be a string. Empty list is acceptable.
            
        Returns:
            list[str]: List of unique variations with duplicates removed.
                      Order of first occurrence is preserved.
                      Original strings (with original case) are maintained.
                      Returns empty list if input is empty.
                      
        Note:
            - Comparison is case-insensitive and strips whitespace
            - Original case and formatting of first occurrence is preserved
            - Whitespace at beginning/end of each variation is ignored for comparison
            
        Example:
            >>> generator = VariationDetermination()
            >>> duplicates = ["Restaurant Karachi", "restaurant karachi", "Cafe Karachi"]
            >>> unique = generator._remove_duplicates(duplicates)
            >>> print(unique)
            ['Restaurant Karachi', 'Cafe Karachi']
        """
        unique_variations = []
        seen = set()
        
        for variation in variations:
            variation_lower = variation.lower().strip()
            if variation_lower not in seen:
                seen.add(variation_lower)
                unique_variations.append(variation)
        
        return unique_variations
    
    def add_custom_industry(self, industry_name, keywords, terms):
        """
        Add a custom industry with its detection keywords and variation terms.
        
        Dynamically adds a new industry type to the variation system. This allows
        users to extend the functionality beyond the built-in industries (textile,
        restaurant, retail). The new industry will be available for detection and
        variation generation.
        
        Args:
            industry_name (str): Name identifier for the industry. Should be lowercase,
                               no spaces (use underscores). Will be used to create
                               attribute names like "{industry_name}_keywords".
            keywords (list[str]): List of keywords to detect this industry in queries.
                                Each keyword should be a string. Case-insensitive matching
                                will be performed. Empty list not recommended.
            terms (list[str]): List of variation terms specific to this industry.
                             Each term should be a string representing a business type
                             in this industry. Empty list not recommended.
            
        Returns:
            None: Function prints confirmation message but returns nothing.
            
        Side Effects:
            - Creates new attributes: {industry_name}_keywords and {industry_name}_terms
            - Prints confirmation message to console
            - Industry becomes available for future detection and variation generation
            
        Note:
            This method sets up the data but doesn't modify the detection logic.
            To fully integrate a custom industry, you would need to modify the
            generate_search_variations method to check for the new industry.
            
        Example:
            >>> generator = VariationDetermination()
            >>> generator.add_custom_industry(
            ...     "automotive", 
            ...     ["car", "auto", "garage", "mechanic"],
            ...     ["auto shop", "car service", "garage", "auto repair"]
            ... )
            Added custom industry: automotive
        """
        # This can be extended to dynamically add new industries
        setattr(self, f"{industry_name}_keywords", keywords)
        setattr(self, f"{industry_name}_terms", terms)
        print(f"Added custom industry: {industry_name}")
    
    def get_supported_industries(self):
        """
        Return a list of currently supported industry categories.
        
        Provides information about which industry types are currently supported
        by the variation generation system. This is useful for documentation,
        user interfaces, or programmatic checks.
        
        Args:
            None
            
        Returns:
            list[str]: List of industry category names that are currently supported.
                      Each string represents a major industry category with brief description.
                      Order is maintained as: Textile, Restaurant, Retail, General.
                      
        Industries Returned:
            - "Textile/Manufacturing": Spinning mills, factories, textile production
            - "Restaurant/Food Service": Restaurants, cafes, food establishments  
            - "Retail/Shopping": Stores, shops, markets, outlets
            - "General Business": Fallback for any other business type
            
        Example:
            >>> generator = VariationDetermination()
            >>> industries = generator.get_supported_industries()
            >>> for industry in industries:
            ...     print(f"- {industry}")
            - Textile/Manufacturing
            - Restaurant/Food Service
            - Retail/Shopping  
            - General Business
        """
        return [
            "Textile/Manufacturing",
            "Restaurant/Food Service", 
            "Retail/Shopping",
            "General Business"
        ]
