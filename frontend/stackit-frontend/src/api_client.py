import requests
from flask import session
from src.config import Config

class APIClient:
    def __init__(self):
        self.base_url = Config.API_BASE_URL
        self.session = requests.Session()
    
    def get_headers(self):
        headers = {'Content-Type': 'application/json'}
        if 'access_token' in session:
            headers['Authorization'] = f"Bearer {session['access_token']}"
        return headers
    
    def get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, headers=self.get_headers(), params=params)
        return response
    
    def post(self, endpoint, data=None):
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, headers=self.get_headers(), json=data)
        return response
    
    def put(self, endpoint, data=None):
        url = f"{self.base_url}{endpoint}"
        response = self.session.put(url, headers=self.get_headers(), json=data)
        return response
    
    def delete(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        response = self.session.delete(url, headers=self.get_headers())
        return response

# Global API client instance
api_client = APIClient()

