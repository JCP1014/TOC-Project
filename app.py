import os
from bottle import route, run, request, abort, static_file

from fsm import TocMachine

PORT = os.environ['PORT']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']

machine = TocMachine(
    states=[
        'user',
        'options',
        # option1
        # option2
        'choosePlace',
        'chooseFood',
        'search',
        'top1',
        'top2'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'options',
            'conditions': 'is_going_to_options'
        },
        # back
        {
            'trigger': 'advance',
            'source': 'options',
            'dest': 'user',
            'conditions': 'is_going_to_last'
        },
        {
            'trigger': 'advance',
            'source': 'options',
            'dest': 'choosePlace',
            'conditions': 'is_going_to_choosePlace'
        },
        # back
        {
            'trigger': 'advance',
            'source': 'choosePlace',
            'dest': 'options',
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
        # back to initial
        {
            'trigger': 'advance',
            'source': [
                'options',
                'choosePlace',
                'chooseFood',
                'search',
                'top1',
                'top2'
            ],
            'dest': 'user',
            'conditions': 'is_going_to_initial'
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
