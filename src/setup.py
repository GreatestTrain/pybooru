from gettext import find
from setuptools import setup, find_packages

NAME = 'PyBooru'
version = '0.45'
description = """
A booru API implementation for python.
"""
author = "Cmoc_edificio"
author_email = "cmoc_edificio@cmoc_edificio.cmoc_edificio"
url = 'https://cmoc.org/cmoc.html'
# packages = ['pybooru', 'classes', 'utils']
packages = find_packages()
# package_dir = {'pybooru': 'src/pybooru',
#                'classes': 'src/pybooru/classes',
#                'utils': 'src/pybooru/utils'}
# package_data = {'pybooru': ''}
install_requires = ['lxml', 'pandas', 'numpy']

setup(name = NAME,
      version = version,
      description=description,
      author=author,
      author_email=author_email,
      url=url,
      packages=packages,
      # package_dir=package_dir,
      install_requires=install_requires,
      python_requires=">=3.10")