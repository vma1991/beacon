error_codes_dict = {
    # 100 : app factory
    '-100': 'No signal header found',
    '-101': 'Invalid signal header',
    '-150': 'Invalid request method',

    # 200 : rss
    # rss_headlines
    '-200': 'Invalid feed url arg',
    '-201': 'Urlopen error',
    '-202': 'Response code was not 200',
    '-203': 'Problematic tags in response text',

    # 300 : google
    # daily_trends
    '-300': 'Urlopen error',
    '-301': 'Response status was not 200',
    '-302': 'Could not JSON decode response',

    # 400 : wikipedia
    # random_page
    '-400': 'Urlopen error',
    '-401': 'Response status was not 200',
    '-402': 'Could not JSON decode response',

    # 500 : steam_top_sellers
    # get_steam_top_sellers
    '-500': 'Instance folder not found',
    '-501': 'Top sellers JSON not found',
    '-502': 'Top sellers JSON error'
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