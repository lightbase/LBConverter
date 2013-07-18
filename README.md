
# Instalação de bibliotecas necessárias:

~$ sudo apt-get install python-uno
~$ sudo apt-get install python-setuptools
~$ sudo apt-get install git

# Para se pegar o repositório:

~$ git init
~$ git clone https://github.com/brenorb/LBConverter.git

# Entre na pasta que foi baixado e instale com o comando:

~$ sudo python setup.py install

# Crie um arquivo development.ini como o modelo e altere as configurações:

[LBConverter]
###Url de acesso à aplicação (usar '/' no fim)
domain: http://0.0.0.0/
###Local do disco onde o arquivo será salvo temporariamente
outpath: /tmp/extract/
###Tempo entre as leituras em busca de registros (em segundos)
sleep_time: 15

[Daemon]
stdin_path = /dev/null
stdout_path = /dev/tty
stderr_path = /dev/tty
pidfile_path = /var/run/lbconverter.pid
logfile_path = /var/log/lbconverter.log
pidfile_timeout = 5

# Para usá-lo basta digitar na pasta do arquivo:

~$ sudo python lbconverter start
~$ sudo python lbconverter stop


