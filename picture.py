import requests
import json5
from util import CACHE_PICTURES_DIR, PIXABAY_CONFIG
import time

class Pictures:
    
    def run(self):
        with open(str(PIXABAY_CONFIG), 'r') as f:
            config = json5.load(f)
            self._uri = config.get("base_url", "https://pixabay.com/api/") + "?key=" + config.get("api_key", "")
            self._uri = self._uri + "&category=" + ",".join(config.get("category", [])) + "&image_type=" + config.get("image_type", "photo") + "&order=" + config.get("order", "popular") + "min_width=" + str(config.get("min_width", 800)) + "&min_height=" + str(config.get("min_height", 1920))  + "&orientation=" + config.get("orientation", "horizontal") + "&per_page=" + str(config.get("per_page", 100)) + "&page=" + str(config.get("page", 1))
            print(self._uri)
        response = requests.get(self._uri)
        if response.status_code != 200: 
            print(f"Failed to fetch data from {self._uri}, status code: {response.status_code}")
        else:
            try:
                # response.text to json
                data_json = response.json()
            except ValueError as e:
                print(f"Failed to parse JSON data: {e}")
        
        if not CACHE_PICTURES_DIR.exists():
            CACHE_PICTURES_DIR.mkdir(parents=True, exist_ok=True)

        for item in data_json["hits"]:
            image_url = item.get("largeImageURL")
            # check if the image URL is valid
            # then get the image_name from the URL of last part split by "/"
            # get image_name, then download and save it to CACHE_PICTURES_DIR
            if image_url:
                image_name = image_url.split("/")[-1]
                image_path = CACHE_PICTURES_DIR / image_name
                if not image_path.exists():
                    try:
                        img_data = requests.get(image_url).content
                        with open(image_path, 'wb') as handler:
                            handler.write(img_data)
                        time.sleep(5) # to avoid hitting the API rate limit
                    except Exception as e:
                        print(f"Failed to download image {image_name}: {e}")

if __name__ == "__main__":
    pictures = Pictures()