#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import time
from daemon import runner
from requests.exceptions import *
import lbconverter
import config
import subprocess
import commands

config.set_config()

#from unoconv import DocumentConverter
#config.CONVERTER = DocumentConverter()    
def run_soffice():
    command = [
        'soffice',
        '--accept="socket,host=localhost,port=%s;urp;StarOffice.Service"' % config.DEFAULT_OPENOFFICE_PORT, 
        '--headless', 
        '--nofirststartwizard'
    ] 
    processes = commands.getoutput('ps -A')
    if not 'soffice' in processes:
        print('calling soffice ... ')
        subprocess.Popen(command)

class App():
   
    def __init__(self):
        self.stdin_path = config.STDIN_PATH
        self.stdout_path = config.STDOUT_PATH
        self.stderr_path = config.STDERR_PATH
        self.pidfile_path =  config.PIDFILE_PATH
        self.pidfile_timeout = config.PIDFILE_TIMEOUT
           
    def run(self):
        while True:
            timeron = time.time()
            #run_soffice()
            try:
                lbconverter.main()
            except (ConnectionError, Timeout) as e:
                logger.error ('Não foi possivel estabelecer conexão com o servidor! ' + config.REST_URL)
            # except:
            #     logger.error ('Erro inesperado')
            timeronff = time.time()
            tempo = (timeronff - timeron)
            tempo = str(tempo)
            str_sleep_time = str(config.SLEEP_TIME)
            logger.info ('Esta execução gastou ' + tempo + ' segundos. Agora uma pausa de ' + str_sleep_time + ' segundos.')
            time.sleep(config.SLEEP_TIME)


# Set up log configurations
logger = logging.getLogger("LBConverter")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.FileHandler(config.LOGFILE_PATH)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Run Daemon
daemon_runner = runner.DaemonRunner(App())
#This ensures that the logger file handle does not get closed during daemonization
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()
