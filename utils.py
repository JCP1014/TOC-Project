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

    shop1 = soup.find('a',attrs={'data-action':'shop_1'})
    name1 = re.sub('\s','',shop1.text)

    url1 = root_url + shop1.get('href')

    img1 = soup.find('img',attrs={'title':name1})
    img1_url = img1.get('src')

    shop2 = soup.find('a',attrs={'data-action':'shop_2'})
    name2 = re.sub('\s','',shop2.text)

    url2 = root_url + shop2.get('href')

    img2 = soup.find('img',attrs={'title':name2})
    img2_url = img2.get('src')

    more_url = search_url + my_params

    address = []
    map_url = []
    items = soup.find_all('span', 'address')
    for i in range(len(items)):
        address.append(items[i].get('data-addr'))
        map_url.append( map_root + address[i] )

    return img1_url, img2_url, name1, name2, url1, url2, map_url, more_url

def show_result_button(place, food, id):
    search_url = 'http://www.ipeen.com.tw/search/taiwan/000/1-0-0-0/'
    img1_url, img2_url, name1, name2, url1, url2, map_url, more_url = search_result(place, food, id)
    send_image_url(id,img1_url)
    send_image_url(id,img2_url)
    buttons = [
                        {
                            "type": "postback",
                            "title": name1,
                            "payload": "top1"
                        },
                        {
                            "type": "postback",
                            "title": name2,
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

def show_info(place,food,id,num):
    img1_url, img2_url, name1, name2, url1, url2, map, more_url = search_result(place,food,id)
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
                            "url": url1,
                            "title": "詳細資料",
                            "webview_height_ratio": "full"
                        }
                    ]
        send_button_message(id,name1,buttons)
    
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
                            "url": url2,
                            "title": "詳細資料",
                            "webview_height_ratio": "full"
                        }
                    ]
        send_button_message(id,name2,buttons)
