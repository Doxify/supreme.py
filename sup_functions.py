import urllib2
import json
from essentials import *

#constant, just the supreme mobile_stock.json url
mobile_stock_url = 'https://www.supremenewyork.com/mobile_stock.json'

#Session function which has the user agent that allows us to spoof a mobile connection
def session(url):
    user_agent = 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko)'
    #Making the request
    session.request = urllib2.Request(url, headers = {'User-Agent' : user_agent})
        
#Release info
def get_release_info():
    #Makes the connection
    session(mobile_stock_url)
    #Reads the output
    response = urllib2.urlopen(session.request).read()
    #Json
    response_json = json.loads(str(response))
    release_week = response_json['release_week']
    release_date = response_json['release_date']
    last_update = response_json['last_mobile_api_update']
    
    logger('info','Release week:' + str(release_week))
    logger('info','Release date:' + str(release_date))
    logger('info', 'Last mobile api update:' + str(last_update))

#Returning information needed for checkout when you input
#a keyword, size, category, and color.
def get_item_info(keyword, category, color, size):
    session(mobile_stock_url)
    response = urllib2.urlopen(session.request).read()
    response_json = json.loads(str(response))
    logger('info', 'Looking up details for "' + keyword + '" in "' + category + '"')
    
    #Getting the item from a dictionary of other items
    for x in response_json['products_and_categories'][category]:
        #If it finds it, it adds it to a variable
        if keyword in x['name'] or keyword == x['name']:
            name = x['name']
            item_id = x['id']
            
            #This gets more specific details needed for checkout, supreme has different
            #ids for every color and size
            if item_id != '':
                session('https://www.supremenewyork.com/shop/' + str(item_id) + '.json')
                response = urllib2.urlopen(session.request).read()
                response_json = json.loads(str(response))
                
                #Going through all the variants
                for x in response_json['styles']:
                    #Checking if the color the user submitted is there, if it is
                    #it gets the style id
                    if x['name'] == color:
                        style_id = x['id']
                        
                        #Checking if the size the user submitted is there, if it is
                        #it gets the size id
                        for x in x['sizes']:
                            if x['name'] == size:
                                size_id = x['id']
                                in_stock = x['stock_level']
                                print
                                logger('info', 'Name: ' + str(name))
                                logger('info', 'Item ID: ' + str(item_id))
                                logger('info', 'Color: ' + str(color))
                                logger('info', 'Style ID: ' + str(style_id))
                                logger('info', 'Size ID: ' + str(size_id))
                                if in_stock == 1:
                                    logger('success', 'Item is in stock')
                                else:
                                    logger('error', 'Item is out of stock')
                                return
                    else:
                        logger('error', 'Color not found')
                        return
        else:
            logger('error', 'Keyword not found')
            return

#get_item_info(keyword, category, color, size)
get_item_info('Pullover', 'new', 'Yellow Camo', 'Large')
