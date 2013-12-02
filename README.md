
LBCONVERTER INSTALLATION

# First install required libs:

openoffice.org-headless
# Please see: http://code.google.com/p/openmeetings/wiki/OpenOfficeConverter#Install_Open_Office_Service_on_Debian/(K)Ubuntu_(versions_>_2)
python2.7
python-uno
python-setuptools

# Install LBConverter:

~$ cd $PATH-TO-LBCONVERTER/LBConverter
IMPORTANT -> Rename the file production.ini-dist to production.ini and make the necessary changes
~$ sudo python setup.py install

# Start OpenOffice process if is not already started:
~$ sudo soffice --accept="socket,host=localhost,port=8100;urp;StarOffice.Service" --headless --nofirststartwizard

# And then start the daemon:

~$ sudo python lbconverter start
~$ sudo python lbconverter stop


