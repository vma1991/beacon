import urllib
import unicodedata



def rss_headlines(args):
    
    try:
        feed_url = args[0]
    except:
        # -202 : invalid feed url arg
        return '-202'
    try:
        n_headlines = args[1]
    except:
        n_headlines = 10
    
    try:
        response = urllib.request.urlopen(feed_url)
    except:
        # return -203 : urlopen error
        return '-203'
    
    if response.status == 200:
        try:
            items = response.read().decode().split('<item>')
        except:
            #-201 : problematic tags in response text
            return '-201'
        
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
        #-200 : response code was not 200
        return -200
