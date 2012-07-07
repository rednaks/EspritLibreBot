#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import socket
import string
import threading
import time
import json



config = {}
configfile = 'config.json'
s=socket.socket()


def Connect():
	s.connect((config['host'], config['port']))
	s.send("NICK %s\r\n" % config['nick'])
	s.send("USER %s %s bla :%s\r\n" % (config['ident'], config['host'], config['realname']))


def GetConfig():
	f = open(configfile,'r')
	fcontent = f.readlines()
	global config 
	config = json.loads(''.join(fcontent))
	f.close()

def joinChannel(msg):
	channel = GetChannel(msg)
	s.send("JOIN %s\r\n" % channel)

def RandMentionResponse():
	return "Did you mention me ? what's up ?! I don't understand human language, so can you speak language I can understand ? Type !help to learn more"

def MakeAction(msg):
	if(msg.find('PRIVMSG') is not -1):
		if(msg.find('hello') >-1 or msg.find('Hello') > -1):
			s.send("PRIVMSG %s :Hello %s :) How are you ? How can I help you ?\r\n" % (GetChannel(msg),GetUname(msg)))
			return
		if(msg.find('EspLibreBot') is not -1):
			s.send("PRIVMSG %s :%s, %s\r\n" % (GetChannel(msg),GetUname(msg),RandMentionResponse())) 
		if(msg.find('!help') is not -1):
			print 'Help cmd detected !'
			s.send("PRIVMSG %s :%s, Sorry, my master is too lasy to implement this :( you can maybe help on https://github.com/rednaks/EspritLibreBot ?\r\n" % (GetChannel(msg),GetUname(msg)))
	if(msg.find('INVITE') is not -1):
		joinChannel(msg)

def GetCmd(msg):
	return

def GetMsg(msg):
  msg = msg[msg.find('PRIVMSG'):]
  msg = msg[msg.find(':')+1:]
  msg = msg[:msg.find('\r')]
  return msg

def GetUname(msg):
  return msg[msg.find(':')+1:msg.find('!')]

def GetChannel(msg):
  if(msg.find('INVITE')>-1):
    return msg[msg.find('#'):msg.find('\r')]
  elif(msg.find('PRIVMSG')>-1):
    msg = msg[msg.find('#'):]
    return msg[:msg.find(':')-1]
  
def printMsg(msg):
  print '@'+GetUname(msg)+': '+GetMsg(msg)

    
def main_loop():
 readbuffer = ""
 while 1:
  readbuffer=readbuffer+s.recv(1024)
  temp=string.split(readbuffer, "\n")
  readbuffer=temp.pop( )
  print temp
  MakeAction(temp[0])
  #print GetMsg(temp[0])
  for line in temp:
      line=string.rstrip(line)
      line=string.split(line)
      if(line[0]=="PING"):
          s.send("PONG %s\r\n" % line[1])
            

if __name__ == '__main__':
	GetConfig()
	Connect()
	main_loop()
