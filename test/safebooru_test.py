from pybooru.classes.booru import GenericBooru
from pybooru.utils.tag_utils import add_tags

import os

def run():
    if not os.path.isdir(os.path.join(os.getcwd(),'mista_bad')):
        os.mkdir('./mista_bad')

    tags = ['walter_white', 'realistic', 'solo']

    config = {
        'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'},
    }

    parameters = {
        'DEFAULT_POST_PAGE_FROM_URL_KW': {
            'post_expr': '//post',
            'attr_expr': '//posts'
        },
        'DEFAULT_POST_PAGE_FROM_JSON_KW': {},
        'DEFAULT_POST_KW': {
            'img_key': 'file_url',
            'preview_key': 'preview_url'
        }
    }

    default_critera = {
        'page': 'dapi',
        's': 'post',
        'q': 'index',
        # 'json': 1,
        'limit': 30,
    }

    wallhaven = GenericBooru('https://safebooru.org',mid='/index.php?', mode='attributes', default_parameters=parameters, default=default_critera)

    print(wallhaven.search_url(
        **{'criteria':
            {'q': add_tags(tags)}},))

    df = wallhaven.fetch_dataframe(
        search_params={'criteria':
            {'tags': add_tags(tags)}},
        save_params={
            'dir_': './mista_bad',
            'save_by': 'file_url',
            'name': 'md5'
        }
    )

    df.to_csv('./walter_white_dataframe.csv')
    
if __name__ == "__main__":
    run()