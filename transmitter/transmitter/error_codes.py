error_codes_dict = {
    # 100 : app factory
    '-100': 'No signal header found',
    '-101': 'Invalid signal header',
    '-150': 'Invalid request method',

    # 200 : rss
    '-200': 'Invalid feed url arg',
    '-201': 'Urlopen error',
    '-202': 'Response code was not 200',
    '-203': 'Problematic tags in response text',

    # 300 : google
    '-300': 'Urlopen error',
    '-301': 'Response status was not 200',
    '-302': 'Could not JSON decode response',

    # 400 : wikipedia
    '-400': 'Urlopen error',
    '-401': 'Response status was not 200',
    '-402': 'Could not JSON decode response'
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