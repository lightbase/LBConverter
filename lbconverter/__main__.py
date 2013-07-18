#!/usr/bin/python
# -*- coding: utf-8 -*-
# To kick off the script, run the following from the python directory:
#   PYTHONPATH=`pwd` python testdaemon.py start

#standard python libs
import logging
import time

#Indexador
from app import main

#third party libs
from daemon import runner
from requests.exceptions import *
import ConfigParser


def setconfig():
    """Função que conecta o modulo ao arquivo de configurações"""

    config = ConfigParser.ConfigParser()
    config.read('development.ini')
    user = {}
    user['domain'] = config.get('LBConverter', 'domain')
    user['outpath'] = config.get('LBConverter', 'outpath')
    user['sleep_time'] = int(config.get('LBConverter', 'sleep_time'))
    user['stdin_path'] = config.get('Daemon', 'stdin_path')
    user['stdout_path'] = config.get('Daemon', 'stdout_path')
    user['stderr_path'] = config.get('Daemon', 'stderr_path')
    user['pidfile_path'] = config.get('Daemon', 'pidfile_path')
    user['logfile_path'] = config.get('Daemon', 'logfile_path')
    user['pidfile_timeout'] = int(config.get('Daemon', 'pidfile_timeout'))
    return user

class App():
   
    def __init__(self):
        self.stdin_path = user['stdin_path']
        self.stdout_path = user['stdout_path']
        self.stderr_path = user['stderr_path']
        self.pidfile_path =  user['pidfile_path']
        self.pidfile_timeout = user['pidfile_timeout']
           
    def run(self):
        while True:
            timeron = time.time()
            logger.info ('Iniciando rotina de extração de texto')
            try:
                main(domain,outpath)

            except (ConnectionError, Timeout):
                logger.error ('Não foi possivel estabelecer conexão com o servidor! ' + domain)
            # except:
            #     logger.error ('Erro inesperado')
            timeronff = time.time()
            tempo = (timeronff - timeron)
            tempo = str(tempo)
            str_sleep_time = str(sleep_time)
            logger.info ('Esta execução gastou ' + tempo + ' segundos. Agora uma pausa de ' + str_sleep_time + ' segundos.')
            time.sleep(sleep_time)

user = setconfig()
domain = user['domain']
sleep_time = user['sleep_time']
outpath = user['outpath']
app = App()
logger = logging.getLogger("LBConverter")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.FileHandler(user['logfile_path'])
handler.setFormatter(formatter)
logger.addHandler(handler)

daemon_runner = runner.DaemonRunner(app)
#This ensures that the logger file handle does not get closed during daemonization
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()
