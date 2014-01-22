
# -*- coding: utf-8 -*-
import os
import sys
import config
import time
import logging
import uno
import datetime
from subprocess import PIPE
from subprocess import Popen
from multiprocessing import Pool
from com.sun.star.task import ErrorCodeIOException
from exception import DocumentConversionException
from exception import UnoConnectionException
from unoconv import DocumentConverter
from unoconv import raise_uno_process
from lbrest import LBRest

def main():
    """
    """

    lbrest = LBRest()
    bases = lbrest.get_bases()
    if bases:
        pool = Pool(processes=len(bases))
        pool.map(convert_files, bases)

def convert_files(args):
    """ Download each file from base and try to extract texts """

    base = args['nome_base']
    extract_time = args['extract_time']

    while(1):
        logger.info('STARTING PROCESS EXECUTION FOR %s' % base)
        # Get initial time
        ti = datetime.datetime.now()

        # Execute process
        raise_uno_process()
        base_converter = BaseConverter(base)
        base_converter.run_conversion()

        # Get final time
        tf = datetime.datetime.now()

        # Calculate interval
        execution_time = tf - ti
        _extract_time = datetime.timedelta(minutes=extract_time)

        if execution_time >= _extract_time:
            interval = 0
        else:
            interval = _extract_time - execution_time

        interval_minutes = (interval.seconds//60)%60

        #logger.info('Finished execution for base %s, will wait for %s minutes' % (base, interval_minutes))
        logger.info('Finished execution for base %s, will wait for %s seconds' % (base, interval.seconds))

        # Sleep interval
        time.sleep(interval.seconds)
        pid = os.getppid()
        if pid == 1:
            logger.info('STOPPING PROCESS EXECUTION FOR %s' % base)
            sys.exit(1)

class BaseConverter():

    def __init__(self, base):
        self.base = base
        self.lbrest = LBRest(base)
        self.files = self.lbrest.get_files()
        self.passed_files = self.lbrest.get_passed_files()

    def is_supported_file(self, id, file_name, file_format):
        if not file_format in config.SUPPORTED_FILES:
            logger.info('File %s , with id %s from base %s is not supported, writing " "' % (file_name, id, self.base))
            self.lbrest.write_text(id, '')
            return False
        return True

    def run_conversion(self):

        for _file in self.files:

            file_name = _file['nome_doc']
            file_format = file_name.split(".")[-1].lower()
            download_url = _file['blob_doc']
            id = download_url.split("/")[-2]

            if id in self.passed_files:
                continue

            if not self.is_supported_file(id, file_name, file_format):
                continue

            logger.info ('Arquivo: base=%s, id=%s, nome=%s' % (self.base, id, file_name))

            local_path = self.lbrest.download(download_url)
            if not local_path:
                continue

            text = self.extract_text(id, file_name, local_path, file_format)
            os.remove(local_path)

            if text:
                self.lbrest.write_text(id, text)

    def extract_text(self, id, file_name, file_path, file_format):
        """ Extract text from file """

        extract_methods = {
            'pdf': self.read_pdf,
            'xml': self.read_textfile,
            'html': self.read_textfile,
            'txt': self.read_textfile
        }

        extract_method = extract_methods.get(file_format, self.read_document)
        return extract_method(id, file_name, file_path, file_format)

    def read_pdf(self, id, file_name, file_path, file_format):
        try:
            process = Popen(["pdftotext", file_path,'-'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
            file_text, err = process.communicate()
            if not file_text:
                raise Exception('Documento pdf possivelmente corrompido ou nao contem texto')
            return file_text or None
        except Exception as exception:
            error_msg= 'Erro ao converter pdf: %s' % exception
            logger.error(error_msg)
            self.lbrest.write_error(id, file_name, error_msg)

    def read_textfile(self, id, file_name, file_path, file_format):
        try:
            with open(file_path) as f:
                file_text = f.read()
            return file_text or None
        except Exception as exception:
            error_msg= 'Erro ao ler arquivo %s : %s' % (file_format, exception)
            logger.error(error_msg)
            self.lbrest.write_error(id, file_name, error_msg)

    def read_document(self, id, file_name, file_path, file_format):
        try:
            converter = DocumentConverter()
            file_text = converter.get_file_text(file_path, file_format)
            return file_text or None
        except UnoConnectionException as exception:
            error_msg= 'UnoConnectionException: %s' % str(exception)
            logger.error(error_msg)
            self.lbrest.write_error(id, file_name, error_msg)
            raise_uno_process()
        except DocumentConversionException as exception:
            error_msg= 'DocumentConversionException: %s' % str(exception)
            logger.error(error_msg)
            self.lbrest.write_error(id, file_name, error_msg)
            raise_uno_process()
        except ErrorCodeIOException as exception:
            error_msg = 'ErrorCodeIOException : %d' % exception.ErrCode
            logger.error(error_msg)
            self.lbrest.write_error(id, file_name, error_msg)
        except Exception as exception:
            error_msg = 'Exception : %s' % exception
            logger.error(error_msg)
            self.lbrest.write_error(id, file_name, error_msg)


logger = logging.getLogger("LBConverter")
