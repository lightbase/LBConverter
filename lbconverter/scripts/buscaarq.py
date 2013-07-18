# -*- coding: utf-8 -*-

from requests import get
from erhandler import is_error
import logging

def listararq(domain,base):
    """Função que lista todos os arquivos a terem o texto extraido"""
    
    # values = {'$$':'{"select":["blob_doc","nome_doc"],"filters":[{"field":"dt_ext_texto","operation":"=","term":null}]}'}
    values = {'$$':'{"select":["blob_doc","nome_doc"],"literal":"dt_ext_texto is null"}'}
    base = str(base)
    url = domain + 'api/doc/' + base
    
    recebe = get(url, params=values)
    logger.debug(recebe._content)
    json_resp = recebe.json()
    er = is_error(url,json_resp)

    arquivos = json_resp["results"]
    return arquivos

    
logger = logging.getLogger("LBConverter")