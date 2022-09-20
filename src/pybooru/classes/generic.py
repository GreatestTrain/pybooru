from dataclasses import dataclass, field
from urllib.parse import urljoin
# import requests
from lxml import html
from urllib.request import Request, urlopen

DEFAULT_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}

@dataclass
class Page:
    url: str
    def __init__(self, url: str, headers=DEFAULT_HEADERS, request_kw: dict = {}):
        self.url = url
        self._dom = None
        self.request_kw = request_kw
        self.headers = headers
    def _visit(self):
        try:
            # r = requests.get(self.url, **config)
            r = urlopen(Request(self.url, headers=self.headers,**self.request_kw))
            if r.getcode() != 200:
                raise Exception
            self._dom = html.fromstring(str(r.read()))
        except Exception as e:
            print(e)
    def jump(self, url):
        return urljoin(self.url, url)
    @property # lazy 
    def dom(self):
        if self._dom is not None:
            return self._dom
        else:
            self._visit()
            return self._dom
    def xpath(self, *args, **kwargs):
        return self.dom.xpath(*args, **kwargs)

@dataclass
class PageWrapper(Page):
    url: str = field(repr=True)
    def __init__(self, url: str, attr: dict = None, headers=DEFAULT_HEADERS, request_kw: dict = {}):
        super(PageWrapper, self).__init__(url, request_kw=request_kw, headers=headers)
        self.attr = attr
    def __getitem__(self, __name: str):
        if __name not in self.attr.keys():
            raise AttributeError('{} is not an attribute of {}'.format(__name, self))
        return self.xpath(self.attr[__name])
    def __iter__(self):
        for key in self.attr.keys():
            yield key, self[key]