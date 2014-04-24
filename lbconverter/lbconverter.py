
# -*- coding: utf-8 -*-
import os
import sys
import config
import time
import logging
import uno
import datetime
import subprocess
import codecs
from requests.exceptions import ConnectionError
from requests.exceptions import Timeout
from subprocess import CalledProcessError
from subprocess import PIPE
from com.sun.star.task import ErrorCodeIOException
from exception import DocumentConversionException
from exception import UnoConnectionException
from unoconv import DocumentConverter
from lbrest import LBRest
import traceback
from imageextractor import extract_pdf_images

def convert_files(args):
    """ Download each file from base and try to extract texts """

    base = args['nome_base']
    extract_time = args['extract_time']

    while True:
        logger.info('STARTING PROCESS EXECUTION FOR %s' % base)

        try:
            base_converter = BaseConverter(base, extract_time)
            base_converter.run_conversion()

        except (ConnectionError, Timeout) as e:
            logger.critical('Could not connect to server! ' + config.REST_URL)

        except Exception as e:
            logger.critical('Uncaught Exception : %s' % traceback.format_exc())

class BaseConverter():

    def __init__(self, base, extract_time):
        self.base = base
        self.extract_time = extract_time
        self.lbrest = LBRest(base)
        self.files = self.lbrest.get_files()
        self.passed_files = self.lbrest.get_passed_files()

    def is_supported_file(self, id, file_name, file_format):
        if not file_format in config.SUPPORTED_FILES:
            logger.info('File %s , with id %s from base %s is not supported, writing " "'\
                % (file_name, id, self.base))
            self.lbrest.write_text(id, '')
            return False
        return True

    def run_conversion(self):

        # Check if Daemon has stopped
        self.check_ppid()

        # Check OpenOffice.org process
        self.run_soffice()

        # Get initial time
        ti = datetime.datetime.now()

        for _file in self.files:

            # Check if Daemon has stopped
            self.check_ppid()

            file_name = _file['nome_doc']
            file_format = file_name.split(".")[-1].lower()
            download_url = _file['blob_doc']
            id_doc = _file['id_doc']
            id_reg = _file['id_reg']

            if str(id_doc) in self.passed_files:
                continue

            if not self.is_supported_file(id_doc, file_name, file_format):
                continue

            logger.info ('Arquivo: base=%s, id_doc=%s, nome=%s' % (self.base, id_doc, file_name))

            local_path = self.lbrest.download(download_url)
            if not local_path:
                continue

            text = self.extract_text(id_doc, id_reg, file_name, local_path, file_format)
            os.remove(local_path)

            if text:
                self.lbrest.write_text(id_doc, text)

        # Get final time
        tf = datetime.datetime.now()
        self.sleep(ti, tf)

    def extract_text(self, id_doc, id_reg, file_name, file_path, file_format):
        """ Extract text from file """

        extract_methods = {
            'pdf': self.read_pdf,
            'xml': self.read_textfile,
            'html': self.read_textfile,
            'txt': self.read_textfile
        }

        extract_method = extract_methods.get(file_format, self.read_document)
        return extract_method(id_doc, id_reg, file_name, file_path, file_format)

    def read_pdf(self, id_doc, id_reg, file_name, file_path, file_format):

        process = subprocess.Popen(["pdftotext", file_path,'-'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
        file_text, error = process.communicate()
        if error:
            error_msg= 'Erro ao converter pdf: Documento pdf possivelmente corrompido'
            logger.error(error_msg)
            self.lbrest.write_error(id_doc, id_reg, file_name, error_msg)

        #'/tmp/<base>-images/file-<50>'
        images_dir = ['/tmp', self.base + '-images', 'file-'+ str(id_doc)].join('/')
        images = extract_pdf_images(file_path, images_dir)

        for idx, image_path in enumerate(images):
            output_path = [images_dir, 'image-' + str(idx)].join('/')
            returncode = process = subprocess.call(["tesseract", '-l', 'por',
                image_path, output_path], stdout=PIPE, stderr=PIPE, stdin=PIPE)
            if returncode == 0:
                with open(output_path) as f:
                    file_text = file_text + '\n' + f.red()
                #os.remove(image_path)
                #os.remove(output_path + '.txt')
            else:
                error_msg= 'Erro ao extrair texto da imagem'
                logger.error(error_msg)

        return file_text

    def read_textfile(self, id_doc, id_reg, file_name, file_path, file_format):
        encoding = self.get_encoding(file_path)
        try:
            with codecs.open(file_path, encoding=encoding) as f:
                file_text = f.read()
            return file_text or None
        except Exception as exception:
            error_msg= 'Erro ao ler arquivo %s : %s' % (file_format, exception)
            logger.error(error_msg)
            self.lbrest.write_error(id_doc, id_reg, file_name, error_msg)

    def read_document(self, id_doc, id_reg, file_name, file_path, file_format):
        try:
            converter = DocumentConverter()
            file_text = converter.get_file_text(file_path, file_format)
            return file_text or None
        except UnoConnectionException as exception:
            error_msg= 'UnoConnectionException: %s' % str(exception)
            logger.error(error_msg)
            self.lbrest.write_error(id_doc, id_reg, file_name, error_msg)
            self.run_soffice()
        except DocumentConversionException as exception:
            error_msg= 'DocumentConversionException: %s' % str(exception)
            logger.error(error_msg)
            self.lbrest.write_error(id_doc, id_reg, file_name, error_msg)
            self.run_soffice()
        except ErrorCodeIOException as exception:
            error_msg = 'ErrorCodeIOException : %d' % exception.ErrCode
            logger.error(error_msg)
            self.lbrest.write_error(id_doc, id_reg, file_name, error_msg)
        except Exception as exception:
            error_msg = 'Exception : %s' % exception
            logger.error(error_msg)
            self.lbrest.write_error(id_doc, id_reg, file_name, error_msg)

    def sleep(self, ti, tf):

        # Calculate interval
        execution_time = tf - ti
        _extract_time = datetime.timedelta(minutes=self.extract_time)

        if execution_time >= _extract_time:
            interval = 0
        else:
            interval = _extract_time - execution_time

        if type(interval) is not int:
            interval_minutes = (interval.seconds//60)%60
            interval_seconds = interval.seconds
        else:
            interval_minutes = interval_seconds = interval

        logger.info('Finished execution for base %s, will wait for %s minutes' 
            % (self.base, str(interval_minutes)))

        # Sleep interval
        time.sleep(interval_seconds)

    def check_ppid(self):
        """ Stop process if daemon is not running
        """
        pid = os.getppid()
        if pid == 1:
            logger.info('STOPPING PROCESS EXECUTION FOR %s' % self.base)
            sys.exit(1)

    def run_soffice(self):
        """ Check if soffice process is running. Case negative, tries to run it.
        """
        try:
            subprocess.check_call('ps -ef | grep -v grep | grep soffice.bin',
                shell=True, stdout=subprocess.PIPE)
        except CalledProcessError:
            command = [
                'soffice',
                '--accept=socket,host=localhost,port=%s;urp;StarOffice.Service' \
                    % config.DEFAULT_OPENOFFICE_PORT,
                '--headless',
                '--nologo',
                '--nofirststartwizard'
            ]
            subprocess.Popen(command, stdout=subprocess.PIPE)
            time.sleep(5)

    def get_encoding(self, file_path):
        """ Guess file encoding
        """
        try:
            output = subprocess.check_output(['file', '--mime-encoding', file_path])
        except (CalledProcessError, OSError) as e:
            logger.error('Could not guess file encoding. Error: %s' % e)
            return None

        encoding = None
        if type(output) is str and len(output.split(':')) > 1:
            encoding = output.split(':')[1]
            try:
                with codecs.open('/dev/null', encoding=encoding) as f:
                    pass
            except LookupError:
                encoding = None

        return encoding

logger = logging.getLogger("LBConverter")
