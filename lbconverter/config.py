

def set_config():

    import ConfigParser

    config = ConfigParser.ConfigParser()
    config.read('development.ini')

    global REST_URL 
    global OUTPATH 
    global DEFAULT_OPENOFFICE_PORT 
    global SLEEP_TIME 
    global STDIN_PATH 
    global STDOUT_PATH 
    global STDERR_PATH 
    global PIDFILE_PATH 
    global LOGFILE_PATH 
    global PIDFILE_TIMEOUT 
    global SUPPORTED_FILES

    #---------------------#
    # Configuration Start #
    #---------------------#

    REST_URL = config.get('LBConverter', 'rest_url')
    OUTPATH = config.get('LBConverter', 'outpath')
    DEFAULT_OPENOFFICE_PORT = int(config.get('LBConverter', 'default_openoffice_port'))
    SLEEP_TIME = int(config.get('LBConverter', 'sleep_time'))
    STDIN_PATH = config.get('Daemon', 'stdin_path')
    STDOUT_PATH = config.get('Daemon', 'stdout_path')
    STDERR_PATH = config.get('Daemon', 'stderr_path')
    PIDFILE_PATH = config.get('Daemon', 'pidfile_path')
    LOGFILE_PATH = config.get('Daemon', 'logfile_path')
    PIDFILE_TIMEOUT = int(config.get('Daemon', 'pidfile_timeout'))
    SUPPORTED_FILES = [
        'doc',
        'docx',
        'odt',
        'rtf',
        'txt',
        'html',
        'pdf',
        'xml',
        #'ods', 
        #'xls', 
        #'xlsx',
        #'ppt',
        #'pptx',
        #'pps',
        #'ppsx',
        #'odp'
    ]

    #-------------------#
    # Configuration End #
    #-------------------#

    global FAMILY_TEXT 
    global FAMILY_WEB 
    global FAMILY_SPREADSHEET 
    global FAMILY_PRESENTATION 
    global FAMILY_DRAWING 

    FAMILY_TEXT = "Text"
    FAMILY_WEB = "Web"
    FAMILY_SPREADSHEET = "Spreadsheet"
    FAMILY_PRESENTATION = "Presentation"
    FAMILY_DRAWING = "Drawing"

    # see http://wiki.services.openoffice.org/wiki/Framework/Article/Filter

    # most formats are auto-detected; only those requiring options are defined here

    global IMPORT_FILTER_MAP 
    IMPORT_FILTER_MAP = {
        "txt": {
            "FilterName": "Text (encoded)",
            "FilterOptions": "utf8"
        },
        "csv": {
            "FilterName": "Text - txt - csv (StarCalc)",
            "FilterOptions": "44,34,0"
        }
    }

    global EXPORT_FILTER_MAP 
    EXPORT_FILTER_MAP = {
        "pdf": {
            FAMILY_TEXT: { "FilterName": "writer_pdf_Export" },
            FAMILY_WEB: { "FilterName": "writer_web_pdf_Export" },
            FAMILY_SPREADSHEET: { "FilterName": "calc_pdf_Export" },
            FAMILY_PRESENTATION: { "FilterName": "impress_pdf_Export" },
            FAMILY_DRAWING: { "FilterName": "draw_pdf_Export" }
        },
        "html": {
            FAMILY_TEXT: { "FilterName": "HTML (StarWriter)" },
            FAMILY_SPREADSHEET: { "FilterName": "HTML (StarCalc)" },
            FAMILY_PRESENTATION: { "FilterName": "impress_html_Export" }
        },
        "odt": {
            FAMILY_TEXT: { "FilterName": "writer8" },
            FAMILY_WEB: { "FilterName": "writerweb8_writer" }
        },
        "doc": {
            FAMILY_TEXT: { "FilterName": "MS Word 97" }
        },
        "docx": {
            FAMILY_TEXT: { "FilterName": "MS Word 2007 XML" }
        },
        "rtf": {
            FAMILY_TEXT: { "FilterName": "Rich Text Format" }
        },
        "txt": {
            FAMILY_TEXT: {
                "FilterName": "Text",
                "FilterOptions": "utf8"
            }
        },
        "ods": {
            FAMILY_SPREADSHEET: { "FilterName": "calc8" }
        },
        "xls": {
            FAMILY_SPREADSHEET: { "FilterName": "MS Excel 97" }
        },
        "csv": {
            FAMILY_SPREADSHEET: {
                "FilterName": "Text - txt - csv (StarCalc)",
                "FilterOptions": "44,34,0"
            }
        },
        "odp": {
            FAMILY_PRESENTATION: { "FilterName": "impress8" }
        },
        "ppt": {
            FAMILY_PRESENTATION: { "FilterName": "MS PowerPoint 97" }
        },
        "swf": {
            FAMILY_DRAWING: { "FilterName": "draw_flash_Export" },
            FAMILY_PRESENTATION: { "FilterName": "impress_flash_Export" }
        }
    }

    global PAGE_STYLE_OVERRIDE_PROPERTIES 
    PAGE_STYLE_OVERRIDE_PROPERTIES = {
        FAMILY_SPREADSHEET: {
            #--- Scale options: uncomment 1 of the 3 ---
            # a) 'Reduce / enlarge printout': 'Scaling factor'
            "PageScale": 100,
            # b) 'Fit print range(s) to width / height': 'Width in pages' and 'Height in pages'
            #"ScaleToPagesX": 1, "ScaleToPagesY": 1000,
            # c) 'Fit print range(s) on number of pages': 'Fit print range(s) on number of pages'
            #"ScaleToPages": 1,
            "PrintGrid": False
        }
    }

