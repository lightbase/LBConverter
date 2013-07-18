# -*- coding: utf-8 -*-

import time

from scripts import erhandler
from scripts import buscabases
from scripts import buscaarq 
from scripts import escreve 
from scripts import fextractor
import logging


def main(domain,outpath):
    """Função principal que busca as bases do banco de dados
    e dentro delas, busca os arquivos que precisam de ter seus
    textos extraídos, os extrai e escreve no texto_doc do banco"""

    lbextractor = '/home/brito/LBConverter/lbextractor.py'
    f_texto = ['doc','docx','odt','rtf','txt','html','pdf']
    
    bases = buscabases.listarbases(domain)
    logger.info("essas sao as bases existentes:")

    erhandler.is_error(domain, bases) #verifica erros
    
    str_bases = str(bases)
    logger.info(str_bases)
         

    for banco in range(0,len(bases)):
        base = bases[banco]['nome_base']
        logger.info("Arquivos que não tiveram o texto extraído da base:")
        logger.info(base)
        results = buscaarq.listararq(domain,base)

        erhandler.is_error(domain, results)
        
        logger.info(results)
        
        for resultado in range(0,len(results)):
            nome = results[resultado]['nome_doc']
            formato = nome.split(".")[-1] 
            logger.debug(formato)
            url = results[resultado]['blob_doc']
        
            if (formato in f_texto):
                logger.info('Começando o processo de extração do texto')
                fextractor.extrator(url,outpath,nome)
            else:

                id_doc = url.split("/")[-2]
                urlbase = 'api/doc/' + base + '/' + id_doc
                texto = 'nulo'
                url1 = domain + urlbase
                logger.info('escrevendo "nulo" na id_doc: ' +
                            id_doc + '\n' + url1)
                f = escreve.escrevetxt(url1, texto)
                time.sleep(0.5)
                logger.info(f)


logger = logging.getLogger("LBConverter")
