# -*- coding: utf-8 -*-

# from requests import get
import urllib
import logging

from erhandler import is_error


def download(url):
    """Função que lista todas as bases"""

    # r = get(url)
    local_path, headers = urllib.urlretrieve (url)

    # logger.debug(headers['content-disposition'].split('filename=')[1])
    # filename = headers['content-disposition'].split('filename=')[1]
    
    # rnome = r.headers['content-disposition']
    # nome = rnome.split()
    is_error(url, local_path)
    return  local_path

logger = logging.getLogger("LBConverter")
