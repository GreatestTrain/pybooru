from genericpath import isdir
from pybooru.classes.booru import GenericBooru
from pybooru.utils.tag_utils import add_tags

import os

def run():
    if not os.path.isdir(os.path.join(os.getcwd(),'wallpapers')):
        os.mkdir('./wallpapers')

    tags = ['landscape', 'sky']
    anti_tags = ['night~', 'anime']

    config = {
        'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'},
    }

    parameters = {
        'DEFAULT_POST_PAGE_FROM_JSON_KW': {
            'post_expr': 'data',
            'attr_expr': 'meta'
        },
        'DEFAULT_POST_KW': {
            'img_key': 'path',
            'preview_key': 'path'
        }
    }

    default_critera = {
        'json': 1,
        'limit': 30,
    }

    wallhaven = GenericBooru('https://wallhaven.cc',mid='/api/v1/search?', mode=None, default_parameters=parameters, default=default_critera)

    print(wallhaven.search_url(
        **{'criteria':
            {'q': add_tags(tags, anti_tags)}},))

    df = wallhaven.fetch_dataframe(
        search_params={'criteria':
            {'q': add_tags(tags, anti_tags)},
            'limit': 4},
        save_params={
            'dir_': './wallpapers',
            'save_by': 'path',
            'name': 'id'
        }
    )

    df.to_csv('./wallpaper_dataframe.csv')
    
if __name__ == '__main__':
    run()