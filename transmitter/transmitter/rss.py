import requests
import unicodedata



def rss_headlines(args):
    
    try:
        feed_url = args[0]
    except:
        # -202 : invalid feed url arg
        return '-202'
    try:
        n_headlines = int(args[1])
    except:
        n_headlines = 10
    
    response = requests.get(feed_url)
    
    if response.status_code == 200:
        try:
            items = response.text.split('<item>')
        except:
            #-201 : problematic tags in response text
            return '-201'
        
        items.pop(0)
        to_return = []
        
        for i in range(min(n_headlines, len(items))):
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
        #-200 : response code was not 200
        return -200
