
# -*- coding: utf-8 -*-

import requests
import logging
import config
from time import sleep
import uuid
import datetime
import json

class LBRest():

    def __init__(self, base=None):
        self.base = base

    def get_bases(self):
        """ Get all bases which has to extract file texts
        """
        bases = None
        params = """{
            "select": [
                "nome_base",
                "extract_time"
            ],
            "literal": "doc_extract is true"
        }"""
        req = requests.get(config.REST_URL, params={'$$':params})
        try:
            req.raise_for_status()
            response = req.json()
            bases = response["results"]
        except:
            logger.error("""
                Erro ao tentar recuperar bases. url: %s. Reposta: %s
            """ % (config.REST_URL, req._content))
        return bases

    def get_files(self):
        """ Get all files which has to convert to text
        """
        files = [ ]
        params = {'$$':'{"select":["blob_doc","nome_doc"],"literal":"dt_ext_texto is null"}'}
        url = config.REST_URL + '/' + self.base + '/doc'
        req = requests.get(url, params=params)
        try:
            req.raise_for_status()
            response = req.json()
            files = response["results"]
        except:
            logger.error("""
                Erro ao tentar recuperar arquivos da base %s. Reposta: %s
            """ % (self.base, req._content))
        return files

    def write_text(self, id, text):
        """ Write extracted text from file to LightBase
        """
        url = config.REST_URL + '/' + self.base + '/doc/' + id + '/text'
        logger.info('Escrevendo texto em : ' + url)
        data = {'texto_doc': text}
        req = requests.put(url, data=data)
        try:
            req.raise_for_status()
        except:
            logger.error("""
                Erro ao tentar alterar texto do arquivo %s da base %s. Reposta: %s
            """ % (str(id), self.base, req._content))

    def download(self, url):
        """Download file from url"""
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
        return local_filename

    def write_error(self, id_doc, file_name, error_msg):
        """ Write errors to LightBase
        """
        error = {
            'base': self.base,
            'id_doc': id_doc,
            'file_name': file_name,
            'error_msg': error_msg,
            'datetime': str(datetime.datetime.now())
        }
        url = config.REST_URL + '/log_lbconverter/reg'
        data = {'json_reg': json.dumps(error)}
        req = requests.post(url, data=data)
        try:
            req.raise_for_status()
        except:
            logger.error("""
                Erro ao tentar escrever erro no Lightbase. Reposta: %s
            """ % req._content)

    def get_passed_files(self):
        """ Get Files that we couldn't get text, so we will not download them again
        """
        passed_files = [ ]
        url = config.REST_URL + '/log_lbconverter/reg'
        params = """{"select": ["id_doc"], "literal": "base = '%s'"}""" % self.base
        req = requests.get(url, params={'$$':params})
        try:
            req.raise_for_status()
            response = req.json()
            passed_files = [ result['id_doc'] for result in response["results"] ]
        except:
            logger.error("""
                Erro ao tentar recuperar documentos que deram erro. Reposta: %s
            """ % req._content)
        return passed_files


logger = logging.getLogger("LBConverter")
