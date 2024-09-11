import os

class Config:
    FLATPAGES_EXTENSION = '.md'
    FLATPAGES_ROOT = os.path.join(os.path.dirname(__file__), 'markdown')
    FLATPAGES_AUTO_RELOAD = True