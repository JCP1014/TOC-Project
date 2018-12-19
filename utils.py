import os
import pymysql
from bs4 import BeautifulSoup
import requests
import urllib
import re
import random

GRAPH_URL = "https://graph.facebook.com/v2.6"
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

ROOT_URL = 'http://www.ipeen.com.tw'
LIST_URL = 'http://www.ipeen.com.tw/search/taiwan/000/1-0-0-0/'
SHOP_PATH = 'shop/'
SPACE_RE = re.compile(r'\s+')

FOOD_NUM = 56
food = [[0 for i in range(6)] for j in range(FOOD_NUM)]
food[0] = ["炒飯",1,1,1,1,1]
food[1] = ["炒麵",1,2,1,1,1]
food[2] = ["鍋燒麵",1,2,2,1,2]
food[3] = ["火鍋",1,3,2,1,2]
food[4] = ["粥",1,1,2,1,2]
food[5] = ["義大利麵",1,2,1,2,2]
food[6] = ["燉飯",1,1,1,2,2]
food[7] = ["漢堡/潛艇堡",1,3,1,2,1]
food[8] = ["自助餐",1,1,1,1,2]
food[9] = ["排骨飯",1,1,1,1,1]
food[10] = ["滷肉飯",1,1,1,1,2]
food[11] = ["丼飯",1,1,1,3,1]
food[12] = ["拉麵",1,2,2,3,2]
food[13] = ["滷味",2,3,1,1,2]
food[14] = ["石鍋拌飯",1,1,1,3,1]
food[15] = ["辛拉麵",1,2,2,3,2]
food[16] = ["炒泡麵",1,2,1,1,1]
food[17] = ["熱壓吐司",2,3,1,2,1]
food[18] = ["鬆餅",2,3,1,2,1]
food[19] = ["水餃",1,3,1,1,2]
food[20] = ["鍋貼",1,3,1,1,1]
food[21] = ["湯餃",1,3,2,1,1]
food[22] = ["肉燥拌麵",1,2,1,1,2]
food[23] = ["餛飩麵",1,2,2,1,2]
food[24] = ["牛肉麵",1,2,2,1,2]
food[25] = ["沙拉",2,3,1,2,2]
food[26] = ["碗粿",1,3,1,1,2]
food[27] = ["米糕",1,1,1,1,2]
food[28] = ["肉圓",1,3,1,1,2]
food[29] = ["抓餅",2,3,1,1,1]
food[30] = ["壽司",2,1,1,3,2]
food[31] = ["蚵仔煎",1,3,1,1,1]
food[32] = ["碳烤",2,3,1,1,2]
food[33] = ["大腸/蚵仔麵線",1,2,2,1,2]
food[34] = ["刀削麵",1,2,1,1,2]
food[35] = ["麻醬麵",1,2,1,1,2]
food[36] = ["米粉",1,3,1,1,1]
food[37] = ["臭豆腐",2,3,1,1,1]
food[38] = ["雞排",2,3,1,1,1]
food[39] = ["麻辣燙",2,3,2,1,2]
food[40] = ["雞蛋糕",2,3,1,1,2]
food[41] = ["鐵板麵",1,2,1,2,1]
food[42] = ["牛排",1,3,1,2,1]
food[43] = ["大阪燒",2,3,1,3,1]
food[44] = ["章魚燒",2,3,1,3,1]
food[45] = ["湯包",1,3,1,1,2]
food[46] = ["關東煮",2,3,2,3,2]
food[47] = ["雞/鴨肉飯",1,1,1,1,2]
food[48] = ["蛋包飯",1,1,1,3,1]
food[49] = ["涼麵",1,2,1,3,2]
food[50] = ["麵疙瘩",1,3,2,1,2]
food[51] = ["披薩",1,3,1,2,2]
food[52] = ["鹽水雞",2,3,1,1,2]
food[53] = ["鹹酥雞",2,3,1,1,1]
food[54] = ["豆花",2,3,2,1,2]
food[55] = ["燒仙草",2,3,2,1,2]


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


    shop1 = soup.find('a',attrs={'data-action':'shop_1'})
    name1 = re.sub('\s','',shop1.text)

    if shop1:
        url1 = root_url + shop1.get('href')
    else:
        status = 0    
    '''
    img1 = soup.find('img',attrs={'title':name1})
    if img1:
        img1_url = img1.get('src')
    else:
        status = 0    
    '''
    shop2 = soup.find('a',attrs={'data-action':'shop_2'})
    name2 = re.sub('\s','',shop2.text)

    if shop2:
        url2 = root_url + shop2.get('href')
    else:
        status = 0    
    '''
    img2 = soup.find('img',attrs={'title':name2})
    if img2:
        img2_url = img2.get('src')
    else:
        status = 0    
    '''
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
        return img, name1, name2, url1, url2, map_url, more_url,status
    else:
        return None, None, None, None, None, None, None, status

def show_result_button(place, food, id):
    search_url = 'http://www.ipeen.com.tw/search/taiwan/000/1-0-0-0/'
    img_url ,name1, name2, url1, url2, map_url, more_url, status = search_result(place, food, id)
    if status==1:
        send_image_url(id,img_url[0])
        send_image_url(id,img_url[1])
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
        return 1
    else:
        send_text_message(id,"搜尋失敗")
        return 0

def show_info(place,food,id,num):
    img_url ,name1, name2, url1, url2, map, more_url, status = search_result(place,food,id)
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
        return 1
    else:
        send_text_message(id,"搜尋失敗")
        return 0

def determine(a1,a2,a3,a4,a5):

    match = 0
    select = []
    for i in range(len(food)):
        if food[i][1] == a1:
            if food[i][2] == a2:
                if food[i][3] == a3:
                    if food[i][4] == a4:
                        if food[i][5] == a5:
                            select.append(food[i][0])
                            match = 1
    
    return match, select

def addToDB(id,col,restaurant):
    db = pymysql.connect("us-cdbr-iron-east-01.cleardb.net","bab38ab676ea34","3fa941dd","heroku_257480eb04565de")
    cursor = db.cursor()
     
    sql = "SELECT * FROM RESTAURANT WHERE USER = %s" % (id)
    try :
        cursor.execute(sql)
        results = cursor.fetchall()
        sql = "UPDATE RESTAURANT SET " + col + " = %s WHERE USER = %s"
        cursor.execute(sql,(restaurant,id))
        db.commit()
    except:
        sql = "INSERT INTO RESTAURANT(USER," + col +") VALUES (%s,%s)"
        cursor.execute(sql,(id,restaurant))
        db.commit()


def show_list(id):
    db = pymysql.connect("us-cdbr-iron-east-01.cleardb.net","bab38ab676ea34","3fa941dd","heroku_257480eb04565de")
    cursor = db.cursor()
 
    _list = ""
    sql = "SELECT * FROM RESTAURANT WHERE USER = %s" % (id)
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        for i in range(len(row)-2):
            if row[i+2]!=None:
                _list += row[i+2] + "\n"
    return _list
        
def random_select():
    index = random.randint(0,FOOD_NUM)
    return food[index][0]
