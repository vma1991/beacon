from logging.config import dictConfig
import os

from flask import Flask, request

from .signals_table import valid_signals
from .error_codes import error_codes_dict, get_error_message
# error codes : 200
from .rss import rss_headlines
# error codes : 300
from .google import daily_trends
# error codes : 400
from .wikipedia import random_page



# error codes : 100
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    


    logfile_path = app.instance_path + '/transmitter.log'
    dictConfig({
        'version': 1,
        'formatters': {
            'default': {
                'format': '%(asctime)s - %(levelname)s - %(message)s',
                'datefmt': '%Y%m%d %H:%M:%S'
            }
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            },
            'rotating_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': logfile_path,
                'maxBytes': 50000,
                'backupCount': 5,
                'formatter': 'default'
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['wsgi', 'rotating_file']
        }
    })



    @app.route('/')
    def dispatcher():

        try:
            remote_addr = request.remote_addr
        except:
            remote_addr = 'remote_addr_error'
        
        headers_dict = dict(request.headers)
        try:
            signal = headers_dict['Signal']
        except:
            # -100 : no signal header found
            app.logger.debug('%s - dispatcher - %s', remote_addr, error_codes.get_error_message('-100'))
            return '-100'
        
        args = []
        i = 0
        while('Arg-'+str(i) in headers_dict):
            args.append(headers_dict['Arg-'+str(i)])
            i = i + 1

            
        
        if request.method == 'GET':

            if signal in valid_signals:
                to_return = eval(signal+'(args)')
                app.logger.debug('%s - %s - %s', remote_addr, signal, get_error_message(to_return))
                return to_return
            
            else:
                # -101 : invalid signal header
                app.logger.debug('%s - dispatcher - %s', remote_addr, get_error_message('-101'))
                return '-101'

        else:
            # -150 : invalid request method
            app.logger.debug('%s - dispatcher - %s', remote_addr, get_error_message('-150'))
            return '-150'

    return app
