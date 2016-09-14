import os
import sys
import json

import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]: # loop over each entry (there may be multiple entries if multiple messages sent at once)
            


            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text
                    message_text = message_text.lower() # convert to lower case

                    #send_message(sender_id, "got it, thanks!")

                    # If we receive a text message, check to see if it matches any special
                    # keywords and send back the corresponding example. Otherwise, just echo
                    # the text we received.
                    special_keywords = {
                        "image": send_image,
                        "gif": send_gif,
                        #"audio": send_audio,
                        #"video": send_video,
                        #"file": send_file,
                        "button": send_button,
                        "generic": send_generic,
                        #"receipt": send_receipt,
                        "quick reply": send_quick_reply,
                        #"read receipt": send_read_receipt,
                        #"typing on": send_typing_on,
                        #"typing off": send_typing_off,
                        #"account linking": send_account_linking
                    }

                    if message_text in special_keywords:
                        special_keywords[message_text](sender_id) # activate the function
                        send_message(sender_id, "got it, thanks!")
                        return "ok", 200
                    else:
                        send_message(sender_id, "got it, thanks!")
                        #page.send(recipient_id, message_text, callback=send_text_callback, notification_type=NotificationType.REGULAR)


                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_image(recipient_id):
    log("sending image to {recipient}".format(recipient=recipient_id))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment":{
            "type":"image",
            "payload":{
            "url": "http://media.topman.com/wcsstore/TopMan/images/catalog/TM83U13MNAV_3col_F_1.jpg"
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def send_gif(recipient_id):
    log("sending gif to {recipient}".format(recipient=recipient_id))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment":{
            "type":"image",
            "payload":{
            "url": "http://cdn.osxdaily.com/wp-content/uploads/2013/07/dancing-banana.gif"
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def send_button(recipient_id):
    log("sending buttons to {recipient}".format(recipient=recipient_id))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":"What do you want to do next?",
                    "buttons":[
                    {
                    "type":"web_url",
                    "url":"https://www.tradesumo.com",
                    "title":"See TradeSumo"
                    },
                    {
                    "type":"postback",
                    "title":"Start Chatting",
                    "payload":"USER_DEFINED_PAYLOAD"
                    }
                    ]
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_generic(recipient_id):
    log("sending generic template to {recipient}".format(recipient=recipient_id))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"generic",
                    "elements":[
                      {
                        "title":"Grilled Cheese & Co",
                        "item_url":"http://www.ilovegrilledcheese.com",
                        "image_url":"http://www.thelogofactory.com/wp-content/uploads/2015/10/grilled-cheese-co-logo.png",
                        "subtitle":"One of life's simple pleasures!",
                        "buttons":[
                          {
                            "type":"web_url",
                            "url":"http://www.ilovegrilledcheese.com",
                            "title":"View Website"
                          },
                          {
                            "type":"postback",
                            "title":"Start Chatting",
                            "payload":"DEVELOPER_DEFINED_PAYLOAD"
                          }              
                        ]
                      },
                      {
                        "title":"Tyto Online",
                        "item_url":"https://www.tytoonline.com",
                        "image_url":"https://www.tytoonline.com/assets/Tyto_Online_Sky_Logo-802ce726f540fa74f9eb5a1dcfcccabe63bffb37212af99f9eb4b709c118c716.png",
                        "subtitle":"Tyto Online is a quest-based, online role-playing game.",
                        "buttons":[
                          {
                            "type":"web_url",
                            "url":"https://www.tytoonline.com",
                            "title":"View Website"
                          },
                          {
                            "type":"postback",
                            "title":"Start Chatting",
                            "payload":"DEVELOPER_DEFINED_PAYLOAD"
                          }              
                        ]
                      },
                      {
                        "title":"Magic Leap",
                        "item_url":"https://www.magicleap.com/#/home",
                        "image_url":"https://www.magicleap.com/img/ml-logo.gif",
                        "subtitle":"Your new way to bring magic back into the world.",
                        "buttons":[
                          {
                            "type":"web_url",
                            "url":"https://www.magicleap.com/#/home",
                            "title":"View Website"
                          },
                          {
                            "type":"postback",
                            "title":"Start Chatting",
                            "payload":"DEVELOPER_DEFINED_PAYLOAD"
                          }              
                        ]
                      }
                    ]
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_quick_reply(recipient_id):
    log("sending quick reply to {recipient}".format(recipient=recipient_id))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message":{
            "text":"Who is the hottest guy in the team?:",
            "quick_replies":[
              {
                "content_type":"text",
                "title":"Ivan",
                "payload":"DEVELOPER_DEFINED_PAYLOAD"
              },
              {
                "content_type":"text",
                "title":"Thang",
                "payload":"DEVELOPER_DEFINED_PAYLOAD"
              },
              {
                "content_type":"text",
                "title":"Boris",
                "payload":"DEVELOPER_DEFINED_PAYLOAD"
              },
              {
                "content_type":"text",
                "title":"Igit",
                "payload":"DEVELOPER_DEFINED_PAYLOAD"
              },
              {
                "content_type":"text",
                "title":"Ramana",
                "payload":"DEVELOPER_DEFINED_PAYLOAD"
              },
            ]
          }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
