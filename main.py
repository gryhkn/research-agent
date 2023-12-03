import trafilatura
import requests
import json

import os
from dotenv import load_dotenv

load_dotenv()
brwoserless_api_key = os.getenv("BROWSERLESS_API_KEY")
serper_api_key = os.getenv("SERP_API_KEY")


def web_search(search_term):
    api_endpoint = "https://google.serper.dev/search"

    # Set up request parameters
    payload = json.dumps({
        "q": search_term
    })

    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }

    # Make the GET request to the search API

    response = requests.request("POST", api_endpoint, headers=headers, data=payload)

    if response.ok:
        search_results = response.json()
        print("Search Results:", search_results)

        return search_results
    else:
        print(f"Error occurred: {response.status_code}")
        return None

web_search("Meta'nın yeni Thread uygulaması nedir?")