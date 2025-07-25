import requests
import json5
from util import CACHE_IMAGES_DIR, PIXABAY_CONFIG, CACHE_DIR, PIXABAY_DOWNLOAED_IMAGE_LIMIT_PER_TIME
import time

class Image:
    
    def __init__(self):
        self.usage_path = CACHE_DIR / "image_usage.json"
        self.usage = {}
        self.load_usage()
    
    def load_usage(self):
        if self.usage_path.exists():
            with open(self.usage_path, 'r') as f:
                self.usage = json5.load(f)

    def save_usage(self):
        with open(self.usage_path, 'w') as f:
            json5.dump(self.usage, f)
    
    def download(self):
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
        
        if not CACHE_IMAGES_DIR.exists():
            CACHE_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

        print("image count:", len(data_json["hits"]))
        download_count = PIXABAY_DOWNLOAED_IMAGE_LIMIT_PER_TIME
        for item in data_json["hits"]:
            if download_count <= 0:
                break
            image_url = item.get("largeImageURL")
            # check if the image URL is valid
            # then get the image_name from the URL of last part split by "/"
            # get image_name, then download and save it to CACHE_IMAGES_DIR
            if image_url:
                image_name = image_url.split("/")[-1]
                image_path = CACHE_IMAGES_DIR / image_name
                if not image_path.exists():
                    try:
                        img_data = requests.get(image_url).content
                        with open(image_path, 'wb') as handler:
                            handler.write(img_data)
                        download_count -= 1
                        time.sleep(5) # to avoid hitting the API rate limit
                    except Exception as e:
                        print(f"Failed to download image {image_name}: {e}")
                # 新下载的图片, 初始化使用次数为0
                if image_name not in self.usage:
                    self.usage[image_name] = 0
        self.save_usage()

if __name__ == "__main__":
    image = Image()
    # image.download_image()
    # 列举 CACHE_IMAGES_DIR 下的所有图片
    for image_path in CACHE_IMAGES_DIR.iterdir():
        image_name = str(image_path).split("\\")[-1]
        if image_name not in image.usage:
            image.usage[image_name] = 0
    print(image.usage)
    image.save_usage()
