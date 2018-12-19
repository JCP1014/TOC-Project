from transitions.extensions import GraphMachine

from utils import send_text_message
from utils import send_button_message
from utils import search_result
from utils import show_result_button
from utils import show_info
from utils import determine
from utils import addToDB
from utils import random_select
from utils import show_list

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )
    def is_going_to_options(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                return text.lower() == 'go to options'
        return 
        
    def is_going_to_q1(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                text = event['postback']['payload']
                return text.lower() == 'option1'
        return False

    def is_going_to_q2(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                text = event['postback']['payload']
                global a1
                a1 = int(text)
                return text.lower() == '1' or text.lower() == '2'
        return False

    def is_going_to_q3(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                text = event['postback']['payload']
                global a2
                a2 = int(text)
                return text.lower() == '1' or text.lower() == '2' or text.lower() == '3'
        return False

    def is_going_to_q4(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                text = event['postback']['payload']
                global a3
                a3 = int(text)
                return text.lower() == '1' or text.lower() == '2'
        return False

    def is_going_to_q5(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                text = event['postback']['payload']
                global a4
                a4 = int(text)
                return text.lower() == '1' or text.lower() == '2' or text.lower() == '3'
        return False

    def is_going_to_determine(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                text = event['postback']['payload']
                global a5
                a5 = int(text)
                return text.lower() == '1' or text.lower() == '2'
        return False

    def is_going_to_redetermine(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                text = event['postback']['payload']
                return text.lower() == 'yes'
        return False

    def is_going_to_giveup(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                text = event['postback']['payload']
                return text.lower() == 'no'
        return False

    #option 2
    def is_going_to_choosePlace(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                text = event['postback']['payload']
                return text.lower() == 'option2'
        return False

    def is_going_to_chooseFood(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                global place
                place  = event['message']['text']
                return place!='' and place!='go to inital' and place!='go to last'
        return False
    
    def is_going_to_search(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                global food
                food  = event['message']['text']
                return food!='' and food!='go to inital' and food!='go to last'
        return False

    def is_going_to_top1(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                text = event['postback']['payload']
                return text.lower() == 'top1'
        return False
    
    def is_going_to_top2(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                text = event['postback']['payload']
                return text.lower() == 'top2'
        return False
    
    # option3
    def is_going_to_setting(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                text = event['postback']['payload']
                return text.lower() == 'option3'
        return False

    def is_going_to_random(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                text = event['postback']['payload']
                return text.lower() == 'random'
        return False

    def is_going_to_rerandom(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                text = event['postback']['payload']
                return text.lower() == 'again'
        return False

    def is_going_to_modify(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                text = event['postback']['payload']
                return text.lower() == 'modify'
        return False

    def is_going_to_add(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                text = event['postback']['payload']
                return text.lower() == 'add'
        return False

    def is_going_to_dele(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                text = event['postback']['payload']
                return text.lower() == 'dele'
        return False

    def is_going_to_list(self, event):
        if event.get("postback"):
            if event['postback'].get('payload'):
                text = event['postback']['payload']
                return text.lower() == 'list'
        return False

    def is_going_to_user(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                return text == '回到主選單' or text == '主選單'
        return False
    
    def is_going_to_last(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                return text.lower() == 'go to last'
        return False

    def on_enter_user(self, event):
        print("I'm entering state1")
        buttons = [
                        {
                            "type": "postback",
                            "title": "幫我想要吃什麼",
                            "payload": "option1"
                        },
                        {
                            "type": "postback",
                            "title": "幫我找店家",
                            "payload": "option2"
                        },
                        {
                            "type": "postback",
                            "title": "從我常去的店家中挑選",
                            "payload": "option3"
                        }
                    ]
        sender_id = event['sender']['id']
        print("sender_id = " + sender_id)
        response = send_button_message(sender_id,"請選擇功能",buttons)
        #addToDB(sender_id,"3",'麥當勞')
        #self.go_back()
    
    def on_enter_q1(self, event):
        print("I'm entering q1")
        buttons = [
                        {
                            "type": "postback",
                            "title": "正餐",
                            "payload": "1"
                        },
                        {
                            "type": "postback",
                            "title": "點心/宵夜",
                            "payload": "2"
                        }
                    ]
        sender_id = event['sender']['id']
        response = send_button_message(sender_id, "要吃正餐還是點心/宵夜呢？",buttons)
        #self.go_back()   

    def on_enter_q2(self, event):
        print("I'm entering q2")
        buttons = [
                        {
                            "type": "postback",
                            "title": "飯",
                            "payload": "1"
                        },
                        {
                            "type": "postback",
                            "title": "麵",
                            "payload": "2"
                        },
                        {
                            "type": "postback",
                            "title": "想吃別的欸",
                            "payload": "3"
                        },
                    ]
        sender_id = event['sender']['id']
        response = send_button_message(sender_id,"想吃飯還是麵呢？",buttons)
        #self.go_back()

    def on_enter_q3(self, event):
        print("I'm entering q3")
        buttons = [
                        {
                            "type": "postback",
                            "title": "不要",
                            "payload": "1"
                        },
                        {
                            "type": "postback",
                            "title": "好阿",
                            "payload": "2"
                        }
                    ]
        sender_id = event['sender']['id']
        response = send_button_message(sender_id, "要吃有湯的嗎？",buttons)
        #self.go_back()

    def on_enter_q4(self, event):
        print("I'm entering q4")
        buttons = [
                        {
                            "type": "postback",
                            "title": "中式",
                            "payload": "1"
                        },
                        {
                            "type": "postback",
                            "title": "西式",
                            "payload": "2"
                        },
                        {
                            "type": "postback",
                            "title": "日式/韓式",
                            "payload": "3"
                        }
                    ]
        sender_id = event['sender']['id']
        response = send_button_message(sender_id, "想吃中式、西式還是日/韓式呢？",buttons)
        #self.go_back()

    def on_enter_q5(self, event):
        print("I'm entering q5")
        buttons = [
                        {
                            "type": "postback",
                            "title": "煎/炒/炸",
                            "payload": "1"
                        },
                        {
                            "type": "postback",
                            "title": "蒸/煮/滷/烤",
                            "payload": "2"
                        }
                    ]
        sender_id = event['sender']['id']
        response = send_button_message(sender_id, "希望是哪種烹調方式呢？",buttons)
        #self.go_back() 

    def on_enter_determine(self, event):
        print("I'm entering determine")
        sender_id = event['sender']['id']
        print(a1,a2,a3,a4,a5)
        match, select = determine(a1,a2,a3,a4,a5)
        if match == 0:
            buttons = [
                        {
                            "type": "postback",
                            "title": "好吧再來一次",
                            "payload": "yes"
                        },
                        {
                            "type": "postback",
                            "title": "算了我還是自己想吧",
                            "payload": "no"
                        }
                    ]
            send_button_message(sender_id, "抱歉我想不到符合您需求的食物耶，要不要試試換個選項？",buttons)
        else:
            send_text_message(sender_id, "我想到的有：\n")
            for i in select:
                send_text_message(sender_id, i + "\n")
            send_text_message(sender_id, "輸入\"回到主選單\"可重新選擇功能")

    def on_enter_choosePlace(self, event):
        print("I'm entering choosePlace")
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "請輸入所在地區")
        #self.go_back()

    def on_enter_chooseFood(self, event):
        print("I'm entering chooseFood")
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "請輸入食物名稱")
        #self.go_back()

    def on_enter_search(self, event):
        print("I'm entering search")
        sender_id = event['sender']['id']
        status = show_result_button(place,food,sender_id)
        send_text_message(sender_id, "輸入\"回到主選單\"可重新選擇功能")
        if status==0:
            self.go_back()
            on_enter_user(self,event)

    def on_enter_top1(self, event):
        print("I'm entering top1")
        sender_id = event['sender']['id']
        show_info(place,food,sender_id,1)
        send_text_message(sender_id, "輸入\"回到主選單\"可重新選擇功能")
    
    def on_enter_top2(self, event):
        print("I'm entering top2")
        sender_id = event['sender']['id']
        show_info(place,food,sender_id,2)
        send_text_message(sender_id, "輸入\"回到主選單\"可重新選擇功能")

    def on_enter_setting(self, event):
        print("I'm entering setting")
        buttons = [
                        {
                            "type": "postback",
                            "title": "隨機挑一間",
                            "payload": "random"
                        },
                        {
                            "type": "postback",
                            "title": "新增或移除店家",
                            "payload": "modify"
                        },
                        {
                            "type": "postback",
                            "title": "查看目前收藏名單",
                            "payload": "list"
                        }
                    ]
        sender_id = event['sender']['id']
        response = send_button_message(sender_id, "我的口袋店家",buttons)
        #self.go_back()

    def on_enter_modify(self, event):
        print("I'm entering modify")

        buttons = [
                        {
                            "type": "postback",
                            "title": "新增",
                            "payload": "add"
                        },
                        {
                            "type": "postback",
                            "title": "移除",
                            "payload": "dele"
                        }
                    ]
        sender_id = event['sender']['id']
        response = send_button_message(sender_id, "輸入\"回到主選單\"可重新選擇功能",buttons)
        #self.go_back()  

    def on_enter_add(self, event):
        print("I'm entering add")
        #self.go_back()  
    
    def on_enter_random(self, event):
        print("I'm entering random")
        food_name = random_select()
        buttons = [
                        {
                            "type": "postback",
                            "title": "不太想欸, 再抽一次",
                            "payload": "again"
                        }
                    ]
        sender_id = event['sender']['id']
        response = send_button_message(sender_id, "那今天吃" + food_name + "怎麼樣呢？",buttons)
        response = send_text_message(sender_id, "輸入\"回到主選單\"可重新選擇功能")
        #self.go_back()  

    def on_enter_list(self, event):
        print("I'm entering list")
        sender_id = event['sender']['id']
        _list = show_list(sender_id)
        send_text_message(sender_id, _list)
        #self.go_back()  

    def on_exit_choosePlace(self,event):
        print('Leaving state2')
    
    def on_exit_chooseFood(self,event):
        print('Leaving state2')

    def on_exit_search(self,event):
        print('Leaving state2')