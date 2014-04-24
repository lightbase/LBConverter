# -*- coding: utf-8 -*-
import logging
import uno
from os.path import abspath, splitext
from com.sun.star.beans import PropertyValue
from com.sun.star.task import ErrorCodeIOException
from com.sun.star.connection import NoConnectException
import config
from exception import DocumentConversionException
from exception import UnoConnectionException
import uuid
import time

class DocumentConverter():
    """ Convert documents extensions
        See: https://github.com/mirkonasato/pyodconverter
    """

    def __init__(self):
        port = config.DEFAULT_OPENOFFICE_PORT
        localContext = uno.getComponentContext()
        resolver = localContext.ServiceManager.createInstanceWithContext(
            "com.sun.star.bridge.UnoUrlResolver", localContext)
        try:
            context = resolver.resolve(
                "uno:socket,host=localhost,port=%s;urp;StarOffice.ComponentContext" % port)
        except NoConnectException:
            error_msg = "failed to connect to OpenOffice.org on port %s" % port
            logger.error(error_msg)
            raise UnoConnectionException, error_msg
        self.desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)

    def get_file_text(self, inputFile, inputExt):

        inputUrl = self._toFileUrl(inputFile)
        loadProperties = config.IMPORT_FILTER_MAP['default']

        if config.IMPORT_FILTER_MAP.has_key(inputExt):
            loadProperties.update(config.IMPORT_FILTER_MAP[inputExt])

        try:
            document = self.desktop.loadComponentFromURL(
                inputUrl, "_blank", 0, self._toProperties(loadProperties))
            document.refresh()
        except Exception as exception:
            raise DocumentConversionException, "Error while loading desktop component: %s" % exception

        document_text = None

        try:
            document_text = document.Text.getString()
        except Exception as exception:
            raise DocumentConversionException, "Error while extracting document text: %s" % exception
        finally:
            document.close(True)

        return document_text

    def _overridePageStyleProperties(self, document, family):
        if config.PAGE_STYLE_OVERRIDE_PROPERTIES.has_key(family):
            properties = config.PAGE_STYLE_OVERRIDE_PROPERTIES[family]
            pageStyles = document.getStyleFamilies().getByName('PageStyles')
            for styleName in pageStyles.getElementNames():
                pageStyle = pageStyles.getByName(styleName)
                for name, value in properties.items():
                    pageStyle.setPropertyValue(name, value)

    def _getStoreProperties(self, document, outputExt):
        family = self._detectFamily(document)
        try:
            propertiesByFamily = config.EXPORT_FILTER_MAP[outputExt]
        except KeyError:
            raise DocumentConversionException, "unknown output format: '%s'" % outputExt
        try:
            return propertiesByFamily[family]
        except KeyError:
            raise DocumentConversionException, "unsupported conversion: from '%s' to '%s'" % (family, outputExt)

    def _detectFamily(self, document):
        if document.supportsService("com.sun.star.text.WebDocument"):
            return config.FAMILY_WEB
        if document.supportsService("com.sun.star.text.GenericTextDocument"):
            # must be TextDocument or GlobalDocument
            return config.FAMILY_TEXT
        if document.supportsService("com.sun.star.sheet.SpreadsheetDocument"):
            return config.FAMILY_SPREADSHEET
        if document.supportsService("com.sun.star.presentation.PresentationDocument"):
            return config.FAMILY_PRESENTATION
        if document.supportsService("com.sun.star.drawing.DrawingDocument"):
            return config.FAMILY_DRAWING
        raise DocumentConversionException, "unknown document family: %s" % document

    def _getFileExt(self, path):
        ext = splitext(path)[1]
        if ext is not None:
            return ext[1:].lower()

    def _toFileUrl(self, path):
        return uno.systemPathToFileUrl(abspath(path))

    def _toProperties(self, dict):
        props = []
        for key in dict:
            prop = PropertyValue()
            prop.Name = key
            prop.Value = dict[key]
            props.append(prop)
        return tuple(props)


logger = logging.getLogger("LBConverter")
