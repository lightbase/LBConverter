# -*- coding: utf-8 -*-

import logging

def is_error(url, jsonfull):
    """Se houver erro de requisição, escreve nos logs"""
    try:
      json = jsonfull.json()
    except:
      logger.debug(jsonfull)
      logger.debug("em " + url)
    else:
      try:
        a = len(json)
      except TypeError:
        id_reg = str(json)
        logger.info('Escrito com sucesso id_reg: ' + id_reg)
      else:
        msg = json['_error_message']
        n_err = str(json['_status'])
        logger.error(n_err + ': ' + msg + " em " + url)


logger = logging.getLogger("LBConverter")