import urllib
import json
import datetime
import re



def traffic_to_int(s):
    s = re.sub(r'K', '000', s)
    s = re.sub(r'M', '000000', s)
    s = re.sub(r'\+', '', s)
    return s


def daily_trends(args):
    try:
        region = args[0]
    except:
        region = 'FR'
    
    regions = ['AR', 'AT', 'AU', 'BE', 'BR', 'CA', 'CH', 'CL', 'CO', 'CZ', 'DE', 'DK', 'EG', 'FI', 
               'GB', 'GR', 'HK', 'HU', 'ID', 'IE', 'IL', 'IN', 'IT', 'JP', 'KE', 'KR', 'MX', 'MY', 
               'NG', 'NL', 'NO', 'NZ', 'PH', 'PL', 'PT', 'RO', 'RU', 'SA', 'SE', 'SG', 'TH', 'TR', 
               'TW', 'UA', 'US', 'VN', 'ZA']
    if region not in regions:
        region = 'FR'
    
    date = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')
    trends_url = 'https://trends.google.com/trends/api/dailytrends?hl=en-US&tz=-12&ed='+date+'&geo='+region+'&ns=15'
    
    try:
        response = urllib.request.urlopen(trends_url)
    except:
        # -300 : urlopen error
        return '-300'
    
    if response.status == 200:
        response_text = response.read().decode()
        if len(response_text.split('\n')) > 1:
            response_text = response_text.split('\n')[1]
        
        decoder = json.JSONDecoder
        try:
            response_dict = decoder().decode(response_text)
        except:
            # -302 : could not JSON decode response
            return '-302'
        
        to_return = []
        for i in range(len(response_dict['default']['trendingSearchesDays'][0]['trendingSearches'])):
            try:
                hits = traffic_to_int(response_dict['default']['trendingSearchesDays'][0]['trendingSearches'][i]['formattedTraffic'])
            except:
                hits = 0
            try:
                query = response_dict['default']['trendingSearchesDays'][0]['trendingSearches'][i]['title']['query']
            except:
                query = 'Error'
            try:
                url = response_dict['default']['trendingSearchesDays'][0]['trendingSearches'][i]['articles'][0]['url']
            except:
                url = '#'        
            to_return.append({'hits': hits, 'query': query, 'url': url})
        
        return to_return
        
    else:
        # -301 : response status was not 200
        return '-301'
    