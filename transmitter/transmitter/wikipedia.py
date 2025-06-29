import urllib
import json



def random_page(args):
    random_url = 'https://fr.wikipedia.org/api/rest_v1/page/random/summary'

    try:
        response = urllib.request.urlopen(random_url)
    except:
        # -400 : urlopen error
        return '-400'
    
    if response.status == 200:
        response_text = response.read().decode()
        decoder = json.JSONDecoder
        try:
            response_dict = decoder().decode(response_text)
        except:
            # -402 : could not JSON decode response
            return '-402'
        
        try:
            title = response_dict['titles']['normalized']
        except:
            title = 'Error'
        try:
            summary = response_dict['extract']
        except:
            summary = 'Error'
        try:
            url = response_dict['content_urls']['desktop']['page']
        except:
            url = '#'
        
        to_return = {'title': title, 'summary': summary, 'url': url}
        return to_return
    
    else:
        # -401 : response status was not 200
        return '-401'
