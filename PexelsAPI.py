import requests
import re

class PexelsAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.pexels.com/v1/"
        self.json = None
        self.headers = {
            "Authorization": self.api_key
        }
    
    def search(self, query, per_page=15, page=1):
        url = self.base_url + "search"
        params = {
            "query": query,
            "per_page": per_page,
            "page": page
        }
        response = requests.get(url, headers=self.headers, params=params)
        try:
            self.json = response.json()
            return response.json()
        except Exception as e:
            print("Error: ", e)
            return None
        
    
    def get_photo(self, id):
        url = self.base_url + "photos/" + str(id)
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    @staticmethod
    def clean_file_name(file_name):
        # Define the regular expression pattern for allowed characters in a file name
        pattern = r'[^a-zA-Z0-9_.-]'
        
        # Remove any characters that are not allowed in a file name
        clean_name = re.sub(pattern, '', file_name)
        
        return clean_name    
    
    """ Download the image from the url and save it to the filename
        @param url: url of the image
        @param filename: filename to save the image
        @size: size of the image:
        "original","large2x","large","medium","small","portrait","landscape","tiny"
    """
    def download(self, url=None, filename=None,size="large2x"):
        if url is None:
            url = self.json["photos"][0]["src"][size]
        if filename is None:
            format = self.json["photos"][0]["src"][size].split(".")[-1].split("?")[0]
            filename = "images/"+PexelsAPI.clean_file_name(self.json["photos"][0]["alt"]+"."+format)
        response = requests.get(url)
        with open(filename, "wb") as file:
            file.write(response.content)
        return filename