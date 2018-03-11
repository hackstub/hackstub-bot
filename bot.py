#!/usr/bin/env python3

# ircecho.py
# Copyright (C) 2011 : Robert L Szkutak II - http://robertszkutak.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import sys
import time
import socket
import string
import shutil
import datetime

HOST = "irc.geeknode.org"
PORT = 6667

NICK = "hackstub-bot"
IDENT = "hackstub-bot"
REALNAME = "hackstub-bot"
MASTER = "Aleks"

readbuffer = ""

s=socket.socket( )
s.connect((HOST, PORT))

s.send(bytes("NICK %s\r\n" % NICK, "UTF-8"))
s.send(bytes("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME), "UTF-8"))

def say(to, message):
    s.send(bytes("PRIVMSG %s %s \r\n" % (to, message), "UTF-8"))

def update(open_, nick, message):
    shutil.copy("./template.html", "./index.html")
    content = open("./index.html").read()
    content = content.replace("{{nickname}}", nick)
    content = content.replace("{{status}}", "ouvert" if open_ else "fermé")
    content = content.replace("{{color}}", "green" if open_ else "red")
    depuis = datetime.datetime.now().strftime("%a %d %B à %H:%M")
    content = content.replace("{{depuis}}", depuis)
    content = content.replace("{{message}}", message)
    open("./index.html", "w").write(content)

while True:
    readbuffer = readbuffer+s.recv(1024).decode("UTF-8")
    temp = str.split(readbuffer, "\n")
    readbuffer=temp.pop( )

    for line in temp:
        print(line)
        line = str.rstrip(line)
        line = str.split(line)

        if(line[0] == "PING"):
            s.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))
        if(line[1] == "PRIVMSG"):
            sender = line[0].strip(":").split("!")[0]
            receiver = line[2]
            message = " ".join(line[3:]).lstrip(":")

            if sender == "Aleks" and message.startswith("!joinhackstub"):
                print("--- Joining chan")
                s.send(bytes("JOIN #Hackstub\r\n", "UTF-8"));

            if receiver == "#HackStub" and message.startswith("!open"):
                message = " ".join(message.split()[1:])
                update(True, sender, message)
                print("--- Opening Hackstub by %s with message : %s" % (sender, message))
                reponse = "(Ok!)"
                say(receiver, reponse)

            if receiver == "#HackStub" and message.startswith("!close"):
                message = " ".join(message.split()[1:])
                update(False, sender, message)
                print("--- Closing hackstub by %s with message : %s" % (sender, message))
                reponse = "(Ok!)"
                say(receiver, reponse)

            if message.startswith("!alarme"):
                say(receiver, "Dude.")

            if message.startswith("!help"):
                say(receiver, "Nope.")

