
class DocumentConversionException(Exception):
    """ Exception when document conversion was not possible.
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class UnoConnectionException(Exception):
    """ Exception when failed to connect to OpenOffice.org
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
