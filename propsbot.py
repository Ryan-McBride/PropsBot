import time
import sqlite3 as lite
import sys
from slackclient import SlackClient


sc = SlackClient(token)


# db initialization
def propsdb(thing, posneg):
  con = lite.connect('props.db')
 
  cursor = con.execute("SELECT * FROM Props WHERE Thing = '{storething}';".format(storething=thing))
  row = cursor.fetchone()

  if row == None:
    if(posneg == "neg"):
      val = -1
    else:
      val = 1
    con.execute("INSERT INTO Props (Thing, Points) VALUES ('{newthing}', 1);".format(newthing=thing))
    con.commit()
  else:
    if(posneg == "neg"):
      val = row[1] - 1
    else:
      val = row[1] + 1
    con.execute("UPDATE Props SET Points = {newval} WHERE Thing = '{storething}';".format(newval=val, storething=thing))
    con.commit()
    
  con.close()
  return val

def sendMess(mess):
  cleanName = mess.replace("+", "").replace("--", "")
  sc.api_call("chat.postMessage", channel=chan, text=cleanName, username="PropsBot", icon_url="https://salesforceyoda.files.wordpress.com/2014/10/fist-slide.jpg")
# function to send message to chat


if sc.rtm_connect():
  print "PropsBot is ready"
  while True:
    events = sc.rtm_read()
    for event in events:
      if event["type"] == "message" and "text" in event: # check for message events
        message = event["text"].split(' ', 1) # split first word out of message
        first = message[0] # get first word
        if(first[-2:] == "++"):
          if(len(message) == 1):
            sendMess("{thing} now has {num} points! :thumbsup:".format(thing=first.encode("utf-8"), num=propsdb(first.replace("+", "").encode("utf-8"), "pos"))) 
          else:
            sendMess("{thing} just got props {reason} for a total of {num} points! :thumbsup:".format(thing=first.encode("utf-8"), reason=message[1].encode("utf-8"), num=propsdb(first.replace("+", "").encode("utf-8"), "pos")))
        elif(first[-2:] == "--"):
          if(len(message) == 1):
            sendMess("{thing} now has {num} points! :thumbsdown:".format(thing=first.encode("utf-8"), num=propsdb(first.replace("-", "").encode("utf-8"), "neg")))
          else:
            sendMess("{thing} just got !props {reason} for a total of {num} points! :thumbsdown:".format(thing=first.encode("utf-8"), reason=message[1].encode("utf-8"), num=propsdb(first.replace("-", "").encode("utf-8"), "neg")))
    time.sleep(1) # timeout for checking new messages
else:
  print "Connection Failed, invalid token?"
