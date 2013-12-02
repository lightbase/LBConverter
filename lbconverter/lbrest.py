
# -*- coding: utf-8 -*-

import requests
import logging
import config
from time import sleep
import uuid

def get_bases():
    """Função que lista todas as bases"""
    bases = None
    params = """{
        "select": [
            "nome_base",
            "extract_time"
        ],
        "literal": "doc_extract is true"
    }"""
    req = requests.get(config.REST_URL, params=params)
    try:
        req.raise_for_status()
        response = req.json()
        bases = response["results"]
    except:
        logger.error("""
            Erro ao tentar recuperar bases. url: %s. Reposta: %s
        """ % (config.REST_URL, req._content))
    return bases
    
def get_files(base):
    """Função que lista todos os arquivos a terem o texto extraido"""
    files = None
    params = {'$$':'{"select":["blob_doc","nome_doc"],"literal":"dt_ext_texto is null"}'}
    url = config.REST_URL + '/' + base + '/doc'
    req = requests.get(url, params=params)
    try:
        req.raise_for_status()
        response = req.json()
        files = response["results"]
    except:
        logger.error("""
            Erro ao tentar recuperar arquivos da base %s. Reposta: %s
        """ % (base, req._content))
    return files

def write_text(base, id, text):
    """Função que escreve o texto no Banco de Dados"""
    url = config.REST_URL + '/' + base + '/doc/' + id + '/text'
    logger.info('Escrevendo texto em : ' + url)
    data = {'texto_doc': text}
    req = requests.post(url, data=data)
    try:
        req.raise_for_status()
    except:
        logger.error("""
            Erro ao tentar alterar texto do arquivo %s da base %s. Reposta: %s
        """ % (str(id), base, req._content))

def download(url):
    """Download file from url"""
    logger.info('Baixando arquivo: %s ...' % url)
    local_path = download_file(url)
    #logger.info('Arquivo salvo em: %s, headers: %s' % (local_path, headers))
    return local_path

def download_file(url):
    local_filename = '/tmp/' + str(uuid.uuid4())
    #http://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py
    req = requests.get(url, stream=True)
    try:
        req.raise_for_status()
    except:
        logger.error("""
            Erro ao tentar baixar arquivo na url %s. Resposta: %s
        """ % (url, req._content))
        return None
    with open(local_filename, 'wb') as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    logger.info('Arquivo salvo em: %s' % local_filename)
    sleep(0.5)
    return local_filename

logger = logging.getLogger("LBConverter")
