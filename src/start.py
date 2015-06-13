#!/usr/bin/env python
# encoding: utf-8

import werobot
try:
    import werobot_token
    _TOKEN = werobot_token._TOKEN
except Exception, e:
    _TOKEN = 'tokenhere'

print "token: " + _TOKEN
robot = werobot.WeRoBot(token=_TOKEN)


@robot.handler
def echo(message):
    print "id: " + str(message.id)
    print "raw: " + message.raw
    print "source: " + message.source
    print "target: " + message.target
    print "time: " + str(message.time)
    print "type: " + message.type


@robot.handler
def echo_text(message):
    if message.type == "text":
        return 'Hello World! Text!'


@robot.handler
def echo_voice(message):
    if message.type == "voice":
        return 'Hello World! Voice!'


@robot.handler
def echo_all(message):
        return 'Hello World! ALL!'


robot.run()
