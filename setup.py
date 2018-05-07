
from setuptools import setup

setup(
    name='the-average-joe',
    version='0.1',
    py_modules=['main'],
    install_requires=[
      'numpy',
      'scipy',
      'sklearn',
      'nltk',
      'aiohttp',
      'aiodns',
      'beautifulsoup4',
      'cchardet',
      'elasticsearch',
      'prettytable'
    ],
)


# pip3 install git+https://git@github.com/ping/instagram_private_api.git@1.5.1