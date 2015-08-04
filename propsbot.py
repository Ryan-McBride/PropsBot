import time
import sqlite3 as lite
import sys
from slackclient import SlackClient

token = ""
sc = SlackClient(token)
chan = ""

# db initialization

def propsdb(thing):
    con = lite.connect('props.db')
   
    cursor = con.execute("SELECT * FROM Props WHERE Thing = '{storething}';".format(storething=thing))
    
    if cursor.fetchone() == None:
      print "if"
      con.execute("INSERT INTO Props (Thing, Points) VALUES ('{newthing}', 1);".format(newthing=thing))
      con.commit()
      #Insert New Row
    else:
      print "else"
      #Increment Existing Row
    
    
    #for row in cursor:
      # print row
    
    con.close()

print sc.api_call("channels.info", channel=chan)

def sendMess(mess):
  cleanName = mess.replace("+", "")
  sc.api_call("chat.postMessage", channel=chan, text=cleanName, username="PropsBot")
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
            propsdb(first.replace("+", "").encode("utf-8"))
            sendMess("{thing} just got props! :thumbsup:".format(thing=first.encode("utf-8"))) 
          else:
            sendMess("{thing} just got props {reason}! :thumbsup:".format(thing=first.encode("utf-8"), reason=message[1].encode("utf-8")))
    time.sleep(1) # timeout for checking new messages
    # TODO: implement a database to keep track of props
else:
  print "Connection Failed, invalid token?"
