import logging
import os
import sys

from webkvm.settings import WS_HOST, WS_PORT, WS_CERT, WS_KEY

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.abspath(os.path.join(DIR_PATH,'..',''))

os.environ.setdefault("DJANGO_SETTINGS_MODULE","webkvm.settings")
CERT = DIR_PATH + '/cer.pem'

if ROOT_PATH not in sys.path:
    sys.path.append(ROOT_PATH)

import Cookie
import socket
import re
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-v",
                  "--verbose",
                  dest="verbose",
                  action="store_true",
                  help="Verbose mode",
                  default=False)

parser.add_option("-d",
                  "--debug",
                  dest="debug",
                  action="store_true",
                  help="Debug mode",
                  default=False)

parser.add_option("-H",
                  "--host",
                  dest="hsot",
                  action="store",
                  help="Listen host",
                  default=WS_HOST)

parser.add_option("-P",
                  "--port",
                  dest="port",
                  action="store",
                  help="Listen port",
                  default=WS_PORT or 6080)

parser.add_option("-c",
                  "--cert",
                  dest="cert",
                  action="store",
                  help="Certificate file path",
                  default=WS_CERT or CERT)

parser.add_option("-k",
                  "--key",
                  dest="key",
                  action="store",
                  help="Certificate key file path",
                  default=WS_KEY)

parser.add_option("--ssl-only",
                  dest="ssl-only",
                  action="store_true",
                  help="Deny non-ssl connections",
                  default=False)

(options,arge) = parser.parse_args()

FORMAT = "%(asctieme)s = %(name)s - %(levelname)s : %(messages)s"

if options.debug:
    logging.basicConfig(level=logging.DEBUG,format=FORMAT)
    options.verbose=True

elif options.verbose:
    logging.basicConfig(level=logging.INFO,format=FORMAT)

else:
    logging.basicConfig(level=logging.WARNING,format=FORMAT)

try:
    from websockify import WebSocketProxy

    try:
        from websockify import ProxyRequestHandler
    except ImportError:
        USE_HANDLER = False
    else:
        USE_HANDLER = True
except ImportError:
    try:
        from null import  WebSocketProxy
        
    except ImportError:
        print('Unable to import a websockify implementation, ' +
              'please install one')
        sys.exit()
    else:
        USE_HANDLER = False
        


        



