from dataclasses import dataclass, field
import re
# import requests
# from io import BytesIO
from urllib.request import Request, urlopen

from base64 import b64encode

from typing import Union

CONTENT_EXPR = re.compile(r'^(?P<type>.+?)/(?P<format>.+?)$')

@dataclass
class Media(object):
    type: str = field(repr=True)
    format: str = field(repr=True)
    def __init__(self, data: Union[bytes, bool] = False, content_type: str = 'unknown', origin='unknown') -> None:
        if data is None:
            raise Exception # <- to do
        self._data = data
        self.content_type = content_type
        self.origin = origin
        self._bytes_generator = None
    @classmethod
    def from_url(cls, url: str, headers: dict = {}, request_kw: dict = {}):
        req = Request(url=url, headers=headers, **request_kw)
        response = urlopen(req)
        content_type = response.headers.get('Content-Type')
        to_return = cls(False, content_type=content_type, origin=response.url)
        to_return._bytes_generator = response.read
        return to_return
    def save(self, name: str):
        with open('{}.{}'.format(name, self.format), 'wb') as f:
            f.write(self.content)
    @property
    def content(self) -> Union[bytes, bool]:
        if not self._data and self._bytes_generator:
            self._data = self._bytes_generator()
        return self._data
    @property
    def type(self) -> str:
        return CONTENT_EXPR.match(self.content_type)['type']
    @property
    def format(self) -> str:
        return CONTENT_EXPR.match(self.content_type)['format']
    def _repr_html_(self) -> str:
        return "<img src={url} />".format(url=self.origin)
    def _bytes_html_(self) -> str:
        return "<img src='data:{content_type};base64,{content}' />".format(content_type=self.content_type,content=b64encode(self.content))