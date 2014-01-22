#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import time
from requests.exceptions import ConnectionError
from requests.exceptions import Timeout
import sys, time
from lbdaemon import Daemon
import lbconverter
import config
import traceback

config.set_config()

# Set up log configurations
logger = logging.getLogger("LBConverter")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.FileHandler(config.LOGFILE_PATH)
handler.setFormatter(formatter)
logger.addHandler(handler)

class LBConverter(Daemon):
    """ Light Base Golden Extractor Daemon
    """

    def run(self):
        """ Overrided method used by super class
        """
        while True:
            try:
                lbconverter.main()
            except (ConnectionError, Timeout) as e:
                logger.error('Não foi possivel estabelecer conexão com o servidor! ' + config.REST_URL)
            except Exception as e:
                logger.critical('UNCAUGHT EXCEPTION : %s' % traceback.format_exc())
                sys.exit(1)

if __name__ == "__main__":

    daemon = LBConverter(config.PIDFILE_PATH)

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print('starting daemon ...')
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
            print('daemon stopped!')
        elif 'restart' == sys.argv[1]:
            daemon.restart()
            print('daemon restarted!')
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)

