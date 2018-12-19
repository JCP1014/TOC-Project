import os
from bottle import route, run, request, abort, static_file

from fsm import TocMachine

PORT = os.environ['PORT']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']

'''
db = pymysql.connect("us-cdbr-iron-east-01.cleardb.net","bab38ab676ea34","3fa941dd","heroku_257480eb04565de")
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print("Database version : %s " % data)
db.close()
'''

machine = TocMachine(
    states=[
        'user',
        # option1
        'q1',
        'q2',
        'q3',
        'q4',
        'q5',
        'determine',
        # option2
        'choosePlace',
        'chooseFood',
        'search',
        'top1',
        'top2',
        # option3
        'setting',
        'random',
        'modify',
        'add',
        'dele',
        'list'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'user',
            'conditions': 'is_going_to_options'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'user',
            'conditions': 'is_going_to_user'
        },
        # option1
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'q1',
            'conditions': 'is_going_to_q1'
        },
        {
            'trigger': 'advance',
            'source': 'q1',
            'dest': 'q2',
            'conditions': 'is_going_to_q2'
        },
        {
            'trigger': 'advance',
            'source': 'q2',
            'dest': 'q3',
            'conditions': 'is_going_to_q3'
        },
        {
            'trigger': 'advance',
            'source': 'q3',
            'dest': 'q4',
            'conditions': 'is_going_to_q4'
        },
        {
            'trigger': 'advance',
            'source': 'q4',
            'dest': 'q5',
            'conditions': 'is_going_to_q5'
        },
        {
            'trigger': 'advance',
            'source': 'q5',
            'dest': 'determine',
            'conditions': 'is_going_to_determine'
        },
        {
            'trigger': 'advance',
            'source': 'determine',
            'dest': 'q1',
            'conditions': 'is_going_to_redetermine'
        },
        {
            'trigger': 'advance',
            'source': 'determine',
            'dest': 'user',
            'conditions': 'is_going_to_giveup'
        },
        # option2
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'choosePlace',
            'conditions': 'is_going_to_choosePlace'
        },
        # back
        {
            'trigger': 'advance',
            'source': 'choosePlace',
            'dest': 'user',
            'conditions': 'is_going_to_last'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'choosePlace',
            'conditions': 'is_going_to_choosePlace'
        },
        # back
        {
            'trigger': 'advance',
            'source': 'choosePlace',
            'dest': 'user',
            'conditions': 'is_going_to_last'
        },
        {
            'trigger': 'advance',
            'source': 'choosePlace',
            'dest': 'chooseFood',
            'conditions': 'is_going_to_chooseFood'
        },
        # back
        {
            'trigger': 'advance',
            'source': 'chooseFood',
            'dest': 'choosePlace',
            'conditions': 'is_going_to_last'
        },
        {
            'trigger': 'advance',
            'source': 'chooseFood',
            'dest': 'search',
            'conditions': 'is_going_to_search'
        },
        # back
        {
            'trigger': 'advance',
            'source': 'search',
            'dest': 'chooseFood',
            'conditions': 'is_going_to_last'
        },
        {
            'trigger': 'advance',
            'source': 'search',
            'dest': 'top1',
            'conditions': 'is_going_to_top1'
        },
        {
            'trigger': 'advance',
            'source': 'top1',
            'dest': 'top2',
            'conditions': 'is_going_to_top2'
        },
        # back
        {
            'trigger': 'advance',
            'source': 'top1',
            'dest': 'search',
            'conditions': 'is_going_to_last'
        },
        {
            'trigger': 'advance',
            'source': 'search',
            'dest': 'top2',
            'conditions': 'is_going_to_top2'
        },
         {
            'trigger': 'advance',
            'source': 'top2',
            'dest': 'top1',
            'conditions': 'is_going_to_top1'
        },
        # back
        {
            'trigger': 'advance',
            'source': 'top2',
            'dest': 'search',
            'conditions': 'is_going_to_last'
        },
        # option3
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'setting',
            'conditions': 'is_going_to_setting'
        },
        # option3-1
        {
            'trigger': 'advance',
            'source': 'setting',
            'dest': 'random',
            'conditions': 'is_going_to_random'
        },
        {
            'trigger': 'advance',
            'source': 'random',
            'dest': 'random',
            'conditions': 'is_going_to_rerandom'
        },
        # option3-3
        {
            'trigger': 'advance',
            'source': 'setting',
            'dest': 'modify',
            'conditions': 'is_going_to_modify'
        },
        {
            'trigger': 'advance',
            'source': 'modify',
            'dest': 'add',
            'conditions': 'is_going_to_add'
        },
        {
            'trigger': 'advance',
            'source': 'modify',
            'dest': 'dele',
            'conditions': 'is_going_to_dele'
        },
        # option3-3
        {
            'trigger': 'advance',
            'source': 'setting',
            'dest': 'list',
            'conditions': 'is_going_to_list'
        },
        # back to initial
        {
            'trigger': 'advance',
            'source': [
                        'user',
                        'q1',
                        'q2',
                        'q3',
                        'q4',
                        'q5',
                        'determine',
                        'choosePlace',
                        'chooseFood',
                        'search',
                        'top1',
                        'top2',
                        'setting',
                        'random',
                        'modify',
                        'add',
                        'dele',
                        'list'
            ],
            'dest': 'user',
            'conditions': 'is_going_to_user'
        },

        {
            'trigger': 'advance',
            'source': [
                        'user',
                        'q1',
                        'q2',
                        'q3',
                        'q4',
                        'q5',
                        'determine',
                        'choosePlace',
                        'chooseFood',
                        'search',
                        'top1',
                        'top2',
                        'random',
                        'modify',
                        'add',
                        'dele',
                        'list'
            ],
            'dest': 'user',
            'conditions': 'is_going_to_options'
        },
        {
            'trigger': 'go_back',
            'source': [

            ],
            'dest': 'user'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)


@route("/webhook", method="GET")
def setup_webhook():
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge

    else:
        abort(403)


@route("/webhook", method="POST")
def webhook_handler():
    body = request.json
    print('\nFSM STATE: ' + machine.state)
    print('REQUEST BODY: ')
    #print(body)

    if body['object'] == "page":
        event = body['entry'][0]['messaging'][0]
        machine.advance(event)
        return 'OK'


@route('/show-fsm', methods=['GET'])
def show_fsm():
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    return static_file('fsm.png', root='./', mimetype='image/png')


if __name__ == "__main__":
    run(host="0.0.0.0", port=PORT, debug=True, reloader=True)
