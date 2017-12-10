import os, sys
from flask import Flask, request
from pprint import pprint
from pymessenger import Bot
from utils import wit_response, get_news_elements

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAFAiY8UdZBYBAJ1TSHLGsIXnwctQ1k1Q5B63SBd6mLZCk9kk3pAFuzebQ8s6lwkXlGF7hFggHA3ZC2dyLLXZAJnZB1MZBy59zuJgXtUZBBVWNALL8DUZBBkZAIuNLA1mH3xhUs3NX8YoGIKFSytLMYTFuQIv1P9fJxDoym8KRR8ptQZDZD"

bot = Bot(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def verify():
    #Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json();
    log(data)

    if data['object'] == 'page':
        for entry in data ['entry']:
            for messaging_event in entry['messaging']:
                #IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text = 'no text'

                    categories = wit_response(messaging_text)
                    elements = get_news_elements(categories)
                    print(categories)
                    bot.send_text_message(sender_id, elements)

    return "ok", 200


def log(message):
    pprint(message)
    sys.stdout.flush()

if __name__ == "__main__":
    app.run(debug = True, port = 80)