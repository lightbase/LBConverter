#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import time
import sys, time
from lbdaemon import Daemon
from lbconverter import convert_files
import config
import traceback
from multiprocessing import Pool
from lbrest import LBRest

config.set_config()

# Set up log configurations
logger = logging.getLogger("LBConverter")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.FileHandler(config.LOGFILE_PATH)
handler.setFormatter(formatter)
logger.addHandler(handler)

class LBConverter(Daemon):
    """ Light Base Extractor Daemon
    """

    def run(self):
        """ Overrided method used by super class.
            Crates a process pool object which controls a pool of worker processes.
            It supports asynchronous results with timeouts and callbacks and has a parallel map implementation.
            That means each base will be processed at same time.
        """
        lbrest = LBRest()
        self.is_running = False
        while not self.is_running:
            bases = lbrest.get_bases()
            if bases:
                self.is_running = True
                try:
                    pool = Pool(processes=len(bases))
                    pool.map(convert_files, bases)
                except Exception as e:
                    logger.critical(str(e))

if __name__ == "__main__":

    daemon = LBConverter(config.PIDFILE_PATH)

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print('starting daemon ...')
            daemon.start()
        elif 'stop' == sys.argv[1]:
            print('stopping daemon ...')
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            print('restarting daemon ...')
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)

