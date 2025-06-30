# GoogleSearchingToTxts

This project is a CLI tool that prompts users for a keyword and searches for results using the Google Maps API. All results are saved to a text file for easy access and analysis.

This project originated from one my bro, who is majoring in Business and wanted a convenient way to gather potential customer information. This is a small but practical tool that will probably be useful in the future. The user interface and more functionalities are on the way (or never).

This project leverages the functionality of the Google Places API (new version). For new or returning users, create or find your own API key and place it in `config.py`. Then run `main.py` from the CLI and follow the instructions. I personally recommend using the enhanced search feature.

## Setup Instructions

1. **Get your API key**: Create or find your own Google Places API key
2. **Configure the project**: 
   - Copy `config_template.py` to `config.py`
   - Replace the placeholder with your actual API key in `config.py`
3. **Run the application**: Execute `main.py` from the CLI and follow the instructions
4. **Recommendation**: Use the enhanced search feature for better results. (However, this will consume the free API call limit at 6x speed.)

## How to Create Your Own API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/) (you need to be logged in with your Google account)
2. Create your own Google Cloud project first
3. Enable the Google Places API(new) for your project
4. Generate an API key and copy it to your `config.py` file. (Note: it's actually `config_template.py` if pulling for the first time)

## API Usage Notice

**Important**: There are usage limits for the Google Places API.

For detailed information about pricing and limits, please check: 
https://developers.google.com/maps/billing-and-pricing/overview

As of June 29, 2025, users can make free API calls under Google's policy, but with limitations. For the exact limits, please check the website above. 

**Recommendation**: Set up billing alerts or usage limits in the Google Cloud Console settings page to protect against unexpected charges.




