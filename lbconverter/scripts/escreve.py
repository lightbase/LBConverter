# -*- coding: utf-8 -*-

from requests import post

from erhandler import is_error
# import urllib


def escrevetxt(url,texto):
    """Função que escreve o texto no Banco de Dados"""
    url = url + "/text"
    values = {'texto_doc':texto}
    f = post(url, data = values)
    
    return f._content
