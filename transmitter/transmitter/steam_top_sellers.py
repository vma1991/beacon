import json
import os

from flask import current_app



def get_steam_top_sellers(args):
    try:
        instance_folder = current_app.instance_path
    except:
        # -500 : instance folder not found
        return '-500'
    
    json_path = instance_folder + '/steam_top_sellers.json'
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r') as f:
                top_sellers_json = json.load(f)
            return top_sellers_json
        except:
            # -502 : top sellers json error
            return '-502'
    
    else:
        # -501 : top sellers json not found
        return '-501'