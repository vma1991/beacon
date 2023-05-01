import os
from flask import Flask, request

# error codes : 200
from . import rss



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
    

    @app.route('/')
    def dispatcher():
        headers_dict = dict(request.headers)
        
        try:
            signal = headers_dict['Signal']
        except:
            # -100 : no signal header found
            return '-100'
        
        args = []
        i = 0
        while('Arg-'+str(i) in headers_dict):
            args.append(headers_dict['Arg-'+str(i)])
            i = i + 1
        
        if request.method == 'GET':
            if signal == 'rss_headlines':
                return rss.rss_headlines(args)
            else:
                # -101 : invalid signal header
                return '-101'
        
        else:
            # -150 : invalid request method
            return '-150'
            
    
    return app
