from transitions.extensions import GraphMachine

from utils import send_text_message
from utils import send_button_message
from utils import search_result
from utils import show_result_button
from utils import show_info

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
        return False

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
    
    def is_going_to_initial(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                return text.lower() == 'go to initial'
        return False
    
    def is_going_to_last(self, event):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                return text.lower() == 'go to last'
        return False

    def on_enter_user(self, event):
        print("I'm inital")
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "I'm initial")
        #self.go_back()

    def on_enter_options(self, event):
        print("I'm entering state1")

        buttons = [
                        {
                            "type": "web_url",
                            "url": "https://www.messenger.com/",
                            "title": "URL Button",
                            "webview_height_ratio": "full"
                        },
                        {
                            "type": "postback",
                            "title": "option2",
                            "payload": "option2"
                        },
                        {
                            "type": "postback",
                            "title": "option3",
                            "payload": "option3"
                        }
                    ]
        sender_id = event['sender']['id']
        response = send_button_message(sender_id, "I'm entering state1",buttons)
        #self.go_back()

    def on_enter_choosePlace(self, event):
        print("I'm entering choosePlace")
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "請輸入所在地區")
        #self.go_back()

    def on_enter_chooseFood(self, event):
        print("I'm entering chooseFood")
        sender_id = event['sender']['id']
        responese = send_text_message(sender_id, "請輸入食物種類")
        #self.go_back()

    def on_enter_search(self, event):
        print("I'm entering search")
        sender_id = event['sender']['id']
        show_result_button(place,food,sender_id)

    def on_enter_top1(self, event):
        print("I'm entering top1")
        sender_id = event['sender']['id']
        show_info(place,food,sender_id,1)
        # self.go_back()
    
    def on_enter_top2(self, event):
        print("I'm entering top2")
        sender_id = event['sender']['id']
        show_info(place,food,sender_id,2)
        # self.go_back()

    def on_exit_options(self,event):
        print('Leaving state1')

    

    def on_exit_choosePlace(self,event):
        print('Leaving state2')
    
    def on_exit_chooseFood(self,event):
        print('Leaving state2')

    def on_exit_search(self,event):
        print('Leaving state2')