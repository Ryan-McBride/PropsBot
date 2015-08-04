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

# sends message to slack
def sendMess(mess):
  cleanName = mess.replace("+", "").replace("--", "")
  sc.api_call("chat.postMessage", channel=chan, text=cleanName, username="PropsBot", icon_url="https://salesforceyoda.files.wordpress.com/2014/10/fist-slide.jpg")

# gets top props list
def getList(num):
  topx = "TOP {amt}:\n".format(amt=num)
  con = lite.connect('props.db')

  cursor = con.execute("SELECT Thing, Points FROM Props ORDER BY Points DESC LIMIT {n};".format(n=num))
  rows = cursor.fetchall()
  for row in rows:
    topx = topx + str(row[1]) + " :\t" + row[0] + "\n"

  sendMess(topx)

# main function
if sc.rtm_connect():
  print "PropsBot is ready"
  while True:
    events = sc.rtm_read()
    for event in events:
      if event["type"] == "message" and "text" in event: # check for message events
        message = event["text"].split(' ', 1) # split first word out of message
        first = message[0] # get first word
        if(len(first) == 2):
          print "no parameters"

        elif(first[-2:] == "++"):
          
          if(len(message) == 1):
            #TODO: Break props messages out into a separate function
            sendMess("{thing} now has {num} points! :thumbsup:".format(thing=first.encode("utf-8"), num=propsdb(first.replace("+", "").encode("utf-8"), "pos"))) 
          else:
            sendMess("{thing} just got props {reason} for a total of {num} points! :thumbsup:".format(thing=first.encode("utf-8"), reason=message[1].encode("utf-8"), num=propsdb(first.replace("+", "").encode("utf-8"), "pos")))
        elif(first[-2:] == "--"):
          if(len(message) == 1):
            sendMess("{thing} now has {num} points! :thumbsdown:".format(thing=first.encode("utf-8"), num=propsdb(first.replace("-", "").encode("utf-8"), "neg")))
          else:
            sendMess("{thing} just got !props {reason} for a total of {num} points! :thumbsdown:".format(thing=first.encode("utf-8"), reason=message[1].encode("utf-8"), num=propsdb(first.replace("-", "").encode("utf-8"), "neg")))
        elif(first == "props.list"):
          if(len(message) == 1):
            getList(5)
          else:
            try:
              val = int(message[1])
              getList(message[1])
            except ValueError:
              sendMess("I need a number for list!")
        elif(first == "props.horn"):
          sendMess("https://www.youtube.com/watch?v=oghDksyOzc8")
        elif(first == "props.holy"):
          sendMess("https://www.youtube.com/watch?v=XNJ1RHUnX9s")
        elif(first == "props.lose"):
          sendMess("https://www.youtube.com/watch?v=1ytCEuuW2_A")
        elif(first == "props.help"):
          sendMess("thingplusplus to give props\nthingminusminus to remove props\nprops.horn for airhorn\nprops.holy for quake sound\nprops.lose for price is right\nprops.help brings up this message")
    time.sleep(1) # timeout for checking new messages
else:
  print "Connection Failed, invalid token?"
