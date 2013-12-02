
# -*- coding: utf-8 -*-
import config
import time
import lbrest
import logging
from subprocess import PIPE
from subprocess import Popen
import uno
from com.sun.star.task import ErrorCodeIOException
from exception import DocumentConversionException
from unoconv import DocumentConverter

def main():
    """Função principal que busca as bases do banco de dados
    e dentro delas, busca os arquivos que precisam de ter seus
    textos extraídos, os extrai e escreve no texto_doc do banco"""

    logger.info ('Iniciando rotina de extração de texto ...')

    bases = lbrest.get_bases()
    if bases:
        for _base in bases:
            base = _base['nome_base']
            base = _base['extract_time']
            logger.info ('Extraindo textos da base %s ...' % base)
            files = lbrest.get_files(base)
            if files:
                extract_base_files(base, files)
            else:
                logger.info ('Nenhum documento encontrado.')

def extract_base_files(base, files):
    """ Download each file from base and try to extract texts """

    for _file in files:

        file_name = _file['nome_doc']
        file_format = file_name.split(".")[-1].lower()
        download_url = _file['blob_doc']
        id = download_url.split("/")[-2]

        logger.info ('Arquivo: id=%s, nome=%s' % (id, file_name))
        if file_format in config.SUPPORTED_FILES:

           logger.info('Começando o processo de extração do texto ...')
           local_path = lbrest.download(download_url)
           if local_path:
               text = extract(local_path, file_format)
               if text:
                   lbrest.write_text(base, id, text)
               else:
                   logger.info('Não foi possível extrair o texto do documento. Escrevendo "" ...')
                   text = ''
                   lbrest.write_text(base, id, text)
                   time.sleep(0.5)
           else:
               logger.info('Não foi possível baixar o documento. Indo para o próximo.')
        else:
            logger.info('Tipo de arquivo não contém texto. Escrevendo "" ...')
            text = ''
            lbrest.write_text(base, id, text)
            time.sleep(0.5)

def extract(file_path, file_format):
    """ Extract text from file """

    file_text = None
    if file_format == 'pdf':
        try:
            logger.debug('Converter pdf. Chamando pdftotext ...')
            process = Popen(["pdftotext", file_path,'-'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
            file_text, err = process.communicate()
        except OSError as err:
            logger.error('Erro ao converter pdf: %s' % err)
    elif file_format == 'xml' or file_format == 'html' or file_format == 'txt':
        try:
            with open(file_path) as f:
                file_text = f.read().decode('utf-8').encode('utf-8')
        except:
            pass
    else:
        try:
            converter = DocumentConverter()
            file_text = converter.get_file_text(file_path, file_format)
        except DocumentConversionException as exception:
            logger.error('DocumentConversionException: %s' % str(exception))
        except ErrorCodeIOException as exception:
            logger.error('ErrorCodeIOException : %d' % exception.ErrCode)

    return file_text

logger = logging.getLogger("LBConverter")
