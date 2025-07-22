import urllib
import json
import os

from flask import current_app



store_ids = [
    "steam_top_sellers",
    "rapport_echo"
]



def json_store(args):
    try:
        instance_folder = current_app.instance_path
    except:
        # -600 : instance folder not found
        return '-600'
    
    try:
        json_id = args[0]
    except:
        # -601 : error getting request args
        return '-601'
    
    if json_id in store_ids:
        json_path = instance_folder + '/store/' + json_id + '.json'
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r') as f:
                    to_return = json.load(f)
                return to_return
            except:
                # -604 : file opening error
                return '-604'
        else:
            # -603 : file not found
            return '-603'
    else:
        # -602 : invalid store id
        return '-602'

