from dataclasses import dataclass, field
from urllib.parse import urlencode, urlparse
from lxml.html import HtmlElement
import json

# local
# from pybooru.utils.tag_utils import add_tags
from pybooru.classes.generic import PageWrapper, Page
from pybooru.classes.image import Media
from pybooru.utils.html_utils import def_elements, fetch_json
# iterables

# analisis
import pandas as pd

DEFAULT_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}

DEFAULT_CONFIG = {
    'headers' : DEFAULT_HEADERS
}

DEFAULT_POST_KW = {
    'img_key': 'file_url',
    'preview_key': 'preview_url',
}

DEFAULT_POST_PAGE_FROM_URL_KW = {
    'post_expr': '//post',
    'attr_expr': '/posts'
}

DEFAULT_POST_PAGE_FROM_JSON_KW = {
    'post_expr': 'post',
    'attr_expr': '@attributes'
}


@dataclass(repr=True)
class Post(dict):
    url: str
    # def __setitem__(self, key, value) -> None:
        # super(Post, dict): 
    def __init__(self, a_dict: dict, img_key: str ='file_url', preview_key: str ='preview_url', config: dict = DEFAULT_CONFIG):
        self._img_key = img_key
        self._preview_key = preview_key
        self.config = config
        # mapping = {key: value for key, value in a_dict.items()}
        super().__init__(a_dict)
    @property
    def url(self) -> str:
        return self[self._img_key]
    @property
    def preview_url(self) -> str:
        return self[self._preview_key]
    @classmethod
    def from_element(cls, element: HtmlElement, mode='descendants', config=DEFAULT_CONFIG,post_kw = DEFAULT_POST_KW):
        mapping = def_elements(element, mode)
        return cls(mapping, config=config,**post_kw)
    @classmethod
    def from_json(cls, a_json_path, img_key='file_url'):
        return cls(json.load(a_json_path), img_key)
    def save(self, dir_: str, name: str = 'md5', save_by: str = 'preview_url'):
        if self.config:
            img = Media.from_url(self[save_by], **self.config)
            location = '{}/{}'.format(dir_, self[name])
            img.save(location)
            return location
        else:
            raise Exception # <- to do
    def _repr_html_(self):
        return "<img src={url} />".format(url=self.preview_url)
    def export(self, save_kw: dict):
        if save_kw:
            location = self.save(**save_kw)
            return self | {'location': location}
        return self


@dataclass
class PostPage(object):
    attributes: dict = field(repr=True)
    def __init__(self, posts: list[Post], attributes: dict['str', 'str'] = {}):
        self.attributes = attributes
        self._posts = posts
    @classmethod
    def from_url(cls, url: str, post_expr='//post', attr_expr='//posts', mode='descendants', config=DEFAULT_CONFIG,post_kw: dict = DEFAULT_POST_KW):
        a_pw = PageWrapper(url, attr={'post': post_expr, 'attributes': attr_expr}, )
        attributes_dict = def_elements(a_pw['attributes'][0], mode='attributes')
        posts_list = map(lambda x: Post.from_element(x, mode=mode,config=config, post_kw=post_kw), a_pw['post'])
        to_return = cls(posts_list, attributes_dict)
        to_return.url = url
        return to_return
    @classmethod
    def from_json(cls, url: str, config: dict = DEFAULT_CONFIG, post_expr='post', attr_expr='@attributes',post_kw: dict = DEFAULT_POST_KW):
        a_dict = fetch_json(url, **config)
        posts_list = map(lambda x: Post(x, config=config, **post_kw) ,a_dict[post_expr])
        return cls(posts_list, a_dict[attr_expr])
    @property
    def posts(self):
        if isinstance(self._posts, map):
            self._posts = list(self._posts)
        return self._posts
    @property
    def __iter__(self):
        return self._posts        
    # check
    def __len__(self):
        return len(self.posts)
    def save(self, dir_: str, name='md5' ,save_by='preview_url'):
        success_counter = 0
        error_counter = 0
        for post in self._posts:
            try:
                post.save(dir_, name, save_by)
                success_counter += 1
            except Exception as e:
                print(post.url, "didn't ", e)
                error_counter += 1
                continue
        return success_counter, error_counter
    def __getitem__(self, __name):
        return self.posts[__name]
    def __repr__(self) -> str:
        return str(self._posts)
    def _repr_html_(self) -> str:
        string = ''
        counter = 0
        for i in self._posts:
            if counter < 5:
                string += ' {}'.format(i._repr_html_())
                counter += 1
            else: break
        return string
    def dataframe(self, save_kw: dict = {}):
        if save_kw:
            function = lambda x: x.export(save_kw).values()
        else:
            function = lambda x: x.values()
        return pd.DataFrame(map(function,self.posts), columns=self[0].export(save_kw).keys())

DEFAULT_CRITERIA = {
    'page': 'dapi',
    's': 'post',
    'q': 'index',
    'pid': 0,
    'json': 1
}

DEFAULT_PARAMETERS = {
    'DEFAULT_POST_KW': DEFAULT_POST_KW,
    'DEFAULT_POST_PAGE_FROM_URL_KW': DEFAULT_POST_PAGE_FROM_URL_KW,
    'DEFAULT_POST_PAGE_FROM_JSON_KW': DEFAULT_POST_PAGE_FROM_JSON_KW
}

@dataclass
class GenericBooru(Page):
    search_query: str = field(repr=True)
    user_id: str = field(repr=False, default=None)
    safe: str = field(repr=False, default='+-~:')
    default: dict = field(repr=True, default_factory=DEFAULT_CRITERIA)
    API_KEY: str = field(repr=True, default=None)
    USER_ID: str = field(repr=True, default=None)
    
    def __init__(self, url: str, mode = None,config: dict = DEFAULT_CONFIG, default = DEFAULT_CRITERIA, API_KEY = None, USER_ID = None, mid = '/index.php?', default_parameters: dict = DEFAULT_PARAMETERS):
        super().__init__(url, **config)
        self.default = default
        self.mode = mode
        self.config = config
        self.mid = mid
        self.API_KEY = API_KEY
        self.USER_ID = USER_ID
        self.default_parameters = default_parameters
    @property
    def api_parameters(self):
        if self.API_KEY and self.USER_ID:
            return {'API_KEY': self.API_KEY, 'USER_ID': self.USER_ID}
        elif self.API_KEY:
            return {'API_KEY', self.API_KEY}
        elif self.USER_ID:
            return {'USER_ID': self.USER_ID}
        else:
            return {}

    def search_url(self, criteria: dict = {}):
        criteria = self.default | criteria
        self.search_query = f'%s{self.mid}%s' % (self.url, urlencode(criteria | self.api_parameters, safe=self.safe))
        return self.search_query
        # print(criteria)
    
    def search_generator(self, criteria: dict = {}, start:int = 0, end:int = 1, limit=100) -> PostPage:
        parameters = criteria | self.default | {'pid': start, 'limit': limit}
        search_url = self.search_url(parameters)
        # print(search_url)
        try:
            sss = parameters['json']
        except:
            sss = False
        while start < end:
            if sss == 1:
                yield PostPage.from_json(search_url, config=self.config, **self.default_parameters['DEFAULT_POST_PAGE_FROM_JSON_KW'],post_kw=self.default_parameters['DEFAULT_POST_KW'])
            else:
                yield PostPage.from_url(search_url, config=self.config, mode=self.mode, **self.default_parameters['DEFAULT_POST_PAGE_FROM_URL_KW'],post_kw=self.default_parameters['DEFAULT_POST_KW'])
            start+=1
    
    # def search(self, criteria: dict = {}, start:int = 0, end:int = 1, limit=100):
    #     a_list = []
    #         for 
    
    def fetch(self, search_params:dict = {}, dir_: str = './out/', name = 'md5',save_by='preview_url'):
        for pagepost in self.search_generator(**search_params):
            pagepost.save(dir_, name, save_by)
            
    def fetch_dataframe(self, search_params: dict = {}, save_params: dict = {}):
        llist = []
        for pagepost in self.search_generator(**search_params):
            llist.append(pagepost.dataframe(save_params))
        df = pd.concat(llist, join='outer').reset_index().drop(columns='index')
        return df