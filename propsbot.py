import time
from slackclient import SlackClient

token = ""
sc = SlackClient(token)
chan = ""

print sc.api_call("channels.info", channel=chan)
# sc.api_call("chat.postMessage", channel="C08H7Q3T6", text="HELLO")

def sendMess(mess):
  sc.api_call("chat.postMessage", channel=chan, text=mess.replace("+", ""), username="PropsBot")
# function to send message to chat

if sc.rtm_connect():
  while True:
    events = sc.rtm_read()
    for event in events:
      if event["type"] == "message" and "text" in event: # check for message events
        message = event["text"].split(' ', 1) # split first word out of message
        first = message[0] # get first word
        if(first[-2:] == "++"):
          if(len(message) == 1):
            sendMess("{thing} just got props! :thumbsup:".format(thing=first.encode("utf-8"))) 
          else:
            sendMess("{thing} just got props {reason}! :thumbsup:".format(thing=first.encode("utf-8"), reason=message[1].encode("utf-8")))
    time.sleep(1) # timeout for checking new messages
    # TODO: implement a database to keep track of props
else:
  print "Connection Failed, invalid token?"
