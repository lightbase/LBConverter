# -*- coding: utf-8 -*-

from requests import get
from erhandler import is_error


def listarbases(domain):
    """Função que lista todas as bases"""

    values = {'$$':'{"select":["nome_base"]}'}
    url = domain + 'api/base'

    recebe = get(url, params=values)
    jsonfull = recebe.json()
    er = is_error(url, jsonfull)

    bases = jsonfull["results"]
    return bases

