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
    """Recebe JSON """
    # url = argv[1]
    # flag = 0
    texto = 'nulo'

    """Pega o URL de download"""
    # url = result['blob_doc']

    # id_doc = url.split("/")[-2]
    # print "id_doc: " + id_doc
    # domain = 'http://neo.lightbase.cc/'
    # base = 'api/doc/arquivos/' + id_doc
    fullurl = url.split("download")[0]

    """Abrindo o arquivo"""
    logger.info(fullurl)
    local_path = download(url)
    sleep(0.5)
    # print(headers['content-disposition'].split('filename=')[1])
    # filename = headers['content-disposition'].split('filename=')[1]
    logger.info( local_path)

    """Se precisar, vai salvar o arquivo aqui"""
    # outpath = '/tmp/extract/'#####################
    """Lembrar de apagar depois"""

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
    # f_planilha = ['xml','ods','csv','pdf']
    # f_apresentacao = ['ppt','pps','odp','pdf']
    # f_imagem = ['jpg','png', 'jpeg', 'tif', 'bmp','pdf']

    if not(formato_in in f_texto):
        logger.warning("Erro: O arquivo de entrada nao e texto!")
        
    if formato_in == 'pdf':
        
        try:
            # print(ifile)
            logger.debug('converter pdf')
            texto = subprocess.call(["pdftotext", local_path,'-'])
            # print(textopdf)
        except OSError as err:
                # handle error (see below)
            logger.error(err)

        
        else:
            infile = infile.split(".")[0]+".txt"
            logger.debug(infile)

    else:
        logger.debug ('iniciando o uno')
        #from scripts import  unotext 
        #from unotext import unoconv

        flag = unoconv(infile, outfile)
        # flag = 1 #Apagar depois, somente teste
        if not flag:
            with open(ofile) as f:
                texto = f.read()

    logger.info ('escrevendo texto')
    # url1 = domain + base
    # print url1

    # req = urllib2.Request(url)
    # r = urllib2.urlopen(req)
    sembarra = fullurl.split('/')
    url1 = sembarra[0]
    for parte in range(1,len(sembarra)-1):
        url1 = url1 + '/' + sembarra[parte] 

    logger.info ('-------' + url1 + '-------')
    f = escrevetxt(url1, texto)
    sleep(0.5)
    logger.info(f)
    

logger = logging.getLogger("LBConverter")
