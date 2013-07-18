# -*- coding: utf-8 -*-

# from requests import get
import urllib
import logging

from erhandler import is_error


def download(url):
    """Função que lista todas as bases"""

    local_path, headers = urllib.urlretrieve (url)
    is_error(url, local_path)
    return  local_path

logger = logging.getLogger("LBConverter")
