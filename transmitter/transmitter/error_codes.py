error_codes_dict = {
    # 100 : app factory
    '-100': 'No signal header found',
    '-101': 'Invalid signal header',
    '-150': 'Invalid request method',

    # 600 : json_store
    '-600': 'Instance folder not found',
    '-601': 'Error getting request args',
    '-602': 'Invalid store id',
    '-603': 'File not found',
    '-604': 'File opening error',

    #700 : rapport_echo
    '-700': 'Instance folder not found',
    '-701': 'Error writing json file'
}



def get_error_message(res):
    try:
        float(res)
    except:
        return 'No errors found'

    if res in error_codes_dict:
        return f'[{res}] {error_codes_dict[res]}'
    else:
        return '[xxx] - Error code not found'