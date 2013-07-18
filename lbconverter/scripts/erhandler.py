# -*- coding: utf-8 -*-

import time
import logging

def is_error(url, jsonfull):
    """Se houver erro de requisição, escreve nos logs"""
    if len(jsonfull) !=4:
        logger.error(url + " jsonfull nao tem 4 parametros")
        erro = True
    elif ('_status' in jsonfull and 
          '_error_message' in jsonfull and 
          '_request' in jsonfull and 
          '_path' in jsonfull):
        logger.error (url + 'não pode ser indexado pelo seguinte motivo: ' + 
                      jsonfull['_status'] + jsonfull['_error_message'])
        erro = True
    else:
        erro = False
    return erro

logger = logging.getLogger("LBConverter")
