# -*- coding: utf-8 -*-
"""Programa em Python criado para converter arquivos


Autor: Breno Rodrigues Brito
e-mail: brenorb@gmail.com"""

from time import sleep
import subprocess
import logging

from unotext import unoconv
from geturl import download
from escreve import escrevetxt

def extrator(url,outpath,filename):
    '''Código que extrai o arquivo filename da url e grava o texto 
    no doc_text do url'''

    texto = 'nulo'

    """Pega o URL de download"""
    fullurl = url.split("download")[0]

    """Abrindo o arquivo"""
    logger.info(fullurl)
    local_path = download(url)
    sleep(0.5)
    logger.info( local_path)

    """Atraves do nome, pega os formatos"""
    formato_in = filename.split(".")[-1]
    fname = filename.split(".")[0]
    formato_out = 'txt'

    logger.info (formato_in +" to "+ formato_out)
    """Formatando para poder abrir os arquivos com o Uno"""
    outfile = "file://" + outpath + fname
    ofile = outpath + fname
    infile = "file://" + local_path

    """Formatos de arquivo"""
    f_texto = ['doc','docx','odt','rtf','txt','html','pdf']
  
    if not(formato_in in f_texto):
        logger.warning("Erro: O arquivo de entrada nao e texto!")
        
    if formato_in == 'pdf':
        # Chama o PDFtoText para converter o arquivo PDF        
        try:
            logger.debug('converter pdf')
            texto = subprocess.call(["pdftotext", local_path,'-'])
        except OSError as err:
            logger.error(err)

        
        else:
            infile = infile.split(".")[0]+".txt"
            logger.debug(infile)

    else:
        logger.debug ('iniciando o uno')
        # Se não for pdf, o uno abre, converte e salva em um arquivo txt
        flag = unoconv(infile, outfile)
        if not flag: # se der certo, ele lê o arquivo e salva o texto
            with open(ofile) as f:
                texto = f.read()

    logger.info ('escrevendo texto')

    sembarra = fullurl.split('/')
    url1 = sembarra[0]
    for parte in range(1,len(sembarra)-1):
        url1 = url1 + '/' + sembarra[parte] 

    logger.info ('-------' + url1 + '-------')
    f = escrevetxt(url1, texto)
    sleep(0.5)
    logger.info(f)
    

logger = logging.getLogger("LBConverter")
