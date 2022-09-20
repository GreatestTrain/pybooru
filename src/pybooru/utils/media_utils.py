import requests
from io import BytesIO
from PIL import Image

def from_url(url, config = dict()):
    r = requests.get(url, **config)
    return BytesIO(r.content)