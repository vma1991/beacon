from urllib.request import Request, urlopen
import json
import unicodedata
import datetime

from flask import current_app



def random_page():
    random_url = 'https://fr.wikipedia.org/api/rest_v1/page/random/summary'
    #mandatory user-agent
    headers = {'User-Agent': 'https://vma1991.net'}
    req = Request(random_url, headers=headers)
    
    try:
        response = urlopen(req)
    except:
        return {'error': 'urlopen error'}
    
    if response.status == 200:
        response_text = response.read().decode()
        decoder = json.JSONDecoder
        try:
            response_dict = decoder().decode(response_text)
        except:
            return {'error': 'could not JSON decode response'}
        
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
        return {'error': 'response status was not 200'}



feed_urls = {
    'ici': 'https://www.francebleu.fr/rss/a-la-une.xml',
    'semur': 'https://www.ville-semur-en-auxois.fr/feed/?post_type=post',
    'lemonde': 'https://www.lemonde.fr/rss/une.xml',
    'mondediplo': 'https://www.monde-diplomatique.fr/recents.xml',
    'courrier': 'https://www.courrierinternational.com/feed/all/rss.xml',
    'bloomberg': 'https://feeds.bloomberg.com/markets/news.rss',
    'ign': 'https://fr.ign.com/feed.xml',
    'equipe': 'https://dwh.lequipe.fr/api/edito/rss'
}



def rss_headlines(feed_url):
    n_headlines = 7
    
    try:
        response = urlopen(feed_url)
    except:
        return {'error': 'urlopen error'}
    
    if response.status == 200:
        try:
            items = response.read().decode().split('<item>')
        except:
            return {'error': 'problematic tags in response text'}
        
        items.pop(0)
        to_return = []
        
        for i in range(min(int(n_headlines), len(items))):
            to_append = {}
            try:
                title = items[i].split('<title>')[1].split('</title>')[0]
            except:
                title = 'Error'
            # handle cdata tags
            try:
                title = title.split('<![CDATA[')[1].split(']]>')[0]
            except:
                pass
                
            try:
                link = items[i].split('<link>')[1].split('</link>')[0]
            except:
                link = '#'
            
            to_append['title'] = unicodedata.normalize('NFKD', title)
            to_append['link'] = link
            to_return.append(to_append)
        
        return to_return
    
    else:
        return {'error': 'response code was not 200'}



def rapport_echo(args):
    try:
        instance_folder = current_app.instance_path
    except:
        # -700 : instance folder not found
        return '-700'
    to_write = {}
    
    # random page
    wikipedia = random_page()
    to_write['wikipedia'] = wikipedia
    
    # rss feeds
    for entry in feed_urls:
        headlines = rss_headlines(feed_urls[entry])
        to_write[entry] = headlines
    
    # timestamp
    now = datetime.datetime.now(datetime.timezone.utc)
    timestamp = now.isoformat()
    to_write['timestamp'] = timestamp

    # save to file
    json_path = instance_folder + '/store/' + 'rapport_echo.json'
    try:
        with open(json_path, 'w') as f:
            json.dump(to_write, f)
        return 'OK'
    except:
        # -701 : error writing json file
        return '-701'




