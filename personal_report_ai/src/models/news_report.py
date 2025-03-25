import requests
import json

class NewsService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.mediastack.com/v1/news"
    def MediaStack_get_news(self, keywords = None, categories = None, countries = None, limit = 10):
        """
        Fetch news articles from MediaStack API
        
        Parameters:
        - keywords: Search term(s)
        - categories: News categories (e.g., business, sports)
        - countries: Countries of news sources (e.g., us, gb)
        - limit: Number of articles to return
        """
        params = {
            'access_key': self.api_key,
            'limit': limit,
        }
        if keywords:
            params['keywords'] = keywords
        if categories:
            params['categorries']= ','.join(categories) if isinstance(categories, list) else categories
        if countries:
            params['countries'] = '.'.join(countries) if isinstance(countries, list) else countries
        response = requests.get(self.base_url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None