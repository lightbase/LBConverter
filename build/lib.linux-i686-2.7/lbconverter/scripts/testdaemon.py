
#To kick off the script, run the following from the python directory:
#   PYTHONPATH=`pwd` python testdaemon.py start

#standard python libs
import logging
import time

#Libs required by Main code
# import urllib2
# import urllib
# import json
# import subprocess
# import time
# from buscabases import listarbases
# from buscaarq import listararq


#third party libs
from daemon import runner

class App():
   
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/var/run/testdaemon/testdaemon.pid'
        self.pidfile_timeout = 5
           
    def run(self):
        while True:
            #Main code goes here ...
           #  with open("config.txt") as f:
           #      tempo = f.read()
           #  t = int(tempo)

           #  domain = 'http://neo.lightbase.cc/'
           # ''' # bases = listarbases(domain)
           #  # print "essas sao as bases existentes:\n"
           #  # print bases
           #  # print '-'*20 
           #  # for base in range(0,len(bases)):
           #  #     print "arquivos que nao tiveram o texto extrido"
           #  #     results = listararq(domain,base)
           #  #     print results
           #  #     print "-"*20'''

            
           #  values = {'$$':'{"select":["blob_doc","nome_doc"],"filters":[{"field":"dt_ext_texto","operation":"=","term":null}]}'}

           #  data = urllib.urlencode(values)

           #  domain = 'http://neo.lightbase.cc/'
           #  base = 'api/doc/arquivos'

           #  url1 = domain + base
           #  url = url1 +'?'+ data.decode('utf-8')
           #  print 'abrindo o url para pegar a base toda'
           #  local_path, headers = urllib.urlretrieve (url)

           #  html = open(local_path)
           #  response = html.read()
           #  print 'aberto, mexendo no json'
           #  json_resp = json.loads(response)
           #  results = json_resp['results']
                
           #  lbextractor = '/home/brito/LBConverter/lbextractor.py'
           #  time.sleep(0.5)
           #  f_texto = ['doc','docx','odt','rtf','txt','html','pdf']
           #  print 'inicia o for'

           #  for result in range(0,len(results)):
           #      nome = results[result]['nome_doc']
           #      formato = nome.split(".")[-1] 
           #      print formato
           #      url = results[result]['blob_doc']
                    
           #      if (formato in f_texto):
           #          print 'extraindo texto'
           #          subprocess.call(["python", lbextractor,url])
           #      else:
           #          print 'escrevendo null'
           #          print url
           #          id_doc = url.split("/")[-2]
           #          domain = 'http://neo.lightbase.cc/'
           #          print(id_doc)
           #          base = 'api/doc/arquivos/' + id_doc
           #          print base
           #          texto = 'null'
           #          values = {'texto_doc':texto, '$method':'PUT'}
           #          data = urllib.urlencode(values)

           #          url1 = domain + base
           #          url = url1 +'?'+ data.decode('utf-8')
           #          print url

           #          # req = urllib2.Request(url)
           #          # r = urllib2.urlopen(req)
           #          f = urllib.urlopen(url1, data)
           #          time.sleep(0.5)
           #          print(f.read())
            #Note that logger level needs to be set to logging.DEBUG before this shows up in the logs
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warn("Warning message")
            logger.error("Error message")
            time.sleep(10)
# arg1 = '"--accept=socket,host=localhost,port=2002;urp;"'
# arg2 = '&'
# subprocess.call(['soffice', arg1, arg2])

app = App()
logger = logging.getLogger("DaemonLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/var/log/testdaemon/testdaemon.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

daemon_runner = runner.DaemonRunner(app)
#This ensures that the logger file handle does not get closed during daemonization
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()
