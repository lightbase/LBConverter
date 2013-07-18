# -*- coding: utf-8 -*-
import logging

import uno
from com.sun.star.beans import PropertyValue


def unoconv(infile, outfile):
    """Abre um arquivo de texto com o uno e o salva como txt"""

    if not flag:
        try:
            subprocess.call(['soffice',
                             '--accept=socket,host=localhost,port=2002;urp;'])
        except:
            logger.error("Possivelmente o StarOffice Uno não está instalado")
        flag = 0
        """Inicializando o PyUno"""
        """Now import the OpenOffice component context. """
        local = uno.getComponentContext()
        """Now access the UnoUrlResolver service. This will allow you to 
        connect to OpenOffice.org program. """
        resolver = local.ServiceManager.createInstanceWithContext(
                                       "com.sun.star.bridge.UnoUrlResolver", local)
        """Now load the context and you are now connected. You can access
         OpenOffice via its API mechanism. """
        context = resolver.resolve(
             "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
        
        """load Desktop service"""
        desktop = context.ServiceManager.createInstanceWithContext(
                                             "com.sun.star.frame.Desktop", context)
        try:
            document = desktop.loadComponentFromURL(infile, "_blank", 0, ())
        except:
            print("Erro: arquivo possivelmente corrompido")
            flag = 1
            pass
        
        if not flag:

            """Needed for FilterName - to export to TXT"""

            TXT = PropertyValue()
            TXT.Name = "FilterName"
            TXT.Value = "Text"
            document.storeAsURL(outfile, (TXT,))    
        
            document.dispose()
    return flag    

logger = logging.getLogger("LBConverter")
