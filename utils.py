import os
from bs4 import BeautifulSoup
import requests
import urllib
import re

GRAPH_URL = "https://graph.facebook.com/v2.6"
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

ROOT_URL = 'http://www.ipeen.com.tw'
LIST_URL = 'http://www.ipeen.com.tw/search/taiwan/000/1-0-0-0/'
SHOP_PATH = 'shop/'
SPACE_RE = re.compile(r'\s+')

def send_text_message(id, text):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {"text": text}
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response


def send_image_url(id, img_url):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message":{
            "attachment": {
                "type":"image",
                "payload":{
                    "url": img_url,
                    "is_reusable":'true'
                }
            }
        }
    }

    response = requests.post(url,json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response


def send_button_message(id, text,buttons):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message":{
            "attachment": {
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":text,
                    "buttons":buttons
                }
            }
        }
    }

    response = requests.post(url,json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response

def search_result(place, food, id):
        
    status = 1
    search_url = 'http://www.ipeen.com.tw/search/taiwan/000/1-0-0-0/'
    root_url = 'http://www.ipeen.com.tw'
    map_root = 'https://www.google.com/maps/place/'
    # search parameters
    my_params = place + ' ' + food
    
    # Download results of google search
    r = requests.get(search_url + my_params)

    # Ensure whether the download is successful
    if r.status_code == requests.codes.ok:
        # Parsing the html source code with Beautifulsoup
        soup = BeautifulSoup(r.text, 'html.parser')
    else:
        status = 0

    '''
    shop1 = soup.find('a',attrs={'data-action':'shop_1'})
    name1 = re.sub('\s','',shop1.text)

    url1 = root_url + shop1.get('href')

    img1 = soup.find('img',attrs={'title':name1})
    if img1:
        img1_url = img1.get('src')
    else:
        status = 0    

    shop2 = soup.find('a',attrs={'data-action':'shop_2'})
    name2 = re.sub('\s','',shop2.text)

    if shop2:
        url2 = root_url + shop2.get('href')
    else:
        status = 0    

    img2 = soup.find('img',attrs={'title':name2})
    if img2:
        img2_url = img2.get('src')
    else:
        status = 0    
    '''

    name = []
    url = []
    items = soup.find_all('a', 'a37 ga_tracking')
    for i in range(len(items)):
        if items[i]:
            name.append(items[i].get('data-shopname'))
            url.append(items[i].get(href))
    img = []
    items = soup.find_all('img', 'lazy')
    for i in range(len(items)):
        if items[i]:
            img.append(items[i].get('src'))

    more_url = search_url + my_params

    address = []
    map_url = []
    items = soup.find_all('span', 'address')
    for i in range(len(items)):
        if items[i]:
            address.append(items[i].get('data-addr'))
            map_url.append( map_root + address[i] )
        else:
            status = 0    

    if status==1:
        return img, name, url, map_url, more_url,status
    else:
        return None, None, None, None, None, None, None, None, status

def show_result_button(place, food, id):
    search_url = 'http://www.ipeen.com.tw/search/taiwan/000/1-0-0-0/'
    img_url ,name, url, map_url, more_url, status = search_result(place, food, id)
    if status==1:
        send_image_url(id,img_url[0])
        send_image_url(id,img_url[1])
        buttons = [
                        {
                            "type": "postback",
                            "title": name[0],
                            "payload": "top1"
                        },
                        {
                            "type": "postback",
                            "title": name[1],
                            "payload": "top2"
                        },
                        {
                            "type": "web_url",
                            "url": more_url,
                            "title": "查看更多",
                            "webview_height_ratio": "full"
                        }
                    ] 
        send_button_message(id,"圖為以下店家",buttons)
        return 1
    else:
        send_text_message(id,"搜尋失敗")
        return 0

def show_info(place,food,id,num):
    img_url ,name, url, map, more_url, status = search_result(place,food,id)
    if status==1:
        if num==1 :    
            buttons = [
                        {
                            "type": "web_url",
                            "url": map[0],
                            "title": "地圖",
                            "webview_height_ratio": "full"
                        },
                        {
                            "type": "web_url",
                            "url": url[0],
                            "title": "詳細資料",
                            "webview_height_ratio": "full"
                        }
                    ]
            send_button_message(id,name[0],buttons)
    
        if num==2 :    
            buttons = [
                        {
                            "type": "web_url",
                            "url": map[1],
                            "title": "地圖",
                            "webview_height_ratio": "full"
                        },
                        {
                            "type": "web_url",
                            "url": url[1],
                            "title": "詳細資料",
                            "webview_height_ratio": "full"
                        }
                    ]
            send_button_message(id,name[1],buttons)
        return 1
    else:
        send_text_message(id,"搜尋失敗")
        return 0
