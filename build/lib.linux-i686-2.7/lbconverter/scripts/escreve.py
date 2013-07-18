# -*- coding: utf-8 -*-

from requests import post

from erhandler import is_error
# import urllib


def escrevetxt(url,texto):
    """Função que escreve o texto no Banco de Dados"""
    url = url + "/text"
    values = {'texto_doc':texto}
    # values = {'texto_doc':texto, '$method':'PUT'}
    # data = urllib.urlencode(values)

	# url1 = domain + base
	# url = url1 +'?'+ data.decode('utf-8')
	# print url

	# req = urllib2.Request(url)
	# r = urllib2.urlopen(req)
    # f = urllib.urlopen(url, data)
    f = post(url, data = values)
    # is_error(url,f)
 #    req = urllib2.Request(url)
	# r = urllib2.urlopen(req)
    
    return f._content
