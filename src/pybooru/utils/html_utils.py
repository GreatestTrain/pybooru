from lxml.html import HtmlElement
from urllib.request import Request, urlopen
import json

DEFAULT_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}

def def_elements(element: HtmlElement, mode):
    a_dict = {}
    match mode:
        case 'descendants':
            for item in element.iterchildren():
                a_dict[item.tag] = item.text
        case 'attributes':
            for tag, text in element.items():
                a_dict[tag] = text
        case _:
            raise Exception
    return a_dict

def fetch_json(url: str, headers=DEFAULT_HEADERS, request_kw: dict = {}):
    r = urlopen(Request(url, headers=headers, **request_kw))
    return json.load(r)