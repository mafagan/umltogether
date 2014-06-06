#!/usr/bin/python
#-*-coding:utf-8-*-
from service import service
from gameSer import game
import sqlite3
import json
__author__ = 'gzs2482'

class info_service(service):
    def __init__(self):
        service.__init__(self)
        commands = {
            3000    : self.activityInit,
            3001    : self.showInfo,
            3002    : self.infoChat,
            3003    : self.togetherAsk,
            3004    : self.togetherReply,
            3005    : self.togetherRes
        }
        self.registers(commands)
        self.init()

    def init(self):
        self.games = []

        for i in range(16):
            self.games.append(game(i))

    def activityInit(self, msg, owner, inputs):
        seatID = msg['seatID']
        pos = msg['pos']
        user = msg['user']
        color = self.games[seatID].addPlayer(user, pos, owner)

        cmd = {
            'id'    : 3000,
            'color' : color
        }
        sendJson = json.dumps(cmd)
        owner.send(sendJson)

    def showInfo(self, msg, owner, inputs):
        seatID = msg['seatID']
        color = msg['color']
        x = msg['x']
        y = msg['y']
        sock = self.games[seatID].getSock()

        cmd = {
            'id'    : 3001,
            'color' : color,
            'x'     : x,
            'y'     : y
        }

        sendJson = json.dumps(cmd)
        for s in sock:
            s.send(sendJson)

    def togetherChat(self, msg, owner, inputs):
        seatID = msg['seatID']
        user = msg['user']
        text = '<p><b>[' + msg['user'] + ' said]:' + '</b></p></ br>' + '  ' + msg['text']

        cmd = {
            'id'    : 3002,
            'text'  : text
        }
        sendJson = json.dumps(cmd)

        sock = self.games[seatID].getSock()
        for s in sock:
            s.send(sendJson)

    def togetherAsk(self, msg, owner, inputs):
        seatID = msg['seatID']
        pos = msg['pos']
        sock = self.games[seatID].getSock()

        cmd = {
            'id'    : 3003
        }
        sendJson = json.dumps(cmd)
        pos = 2 - pos
        sock[pos].send(sendJson)

    def togetherReply(self, msg, owner, inputs):
        seatID = msg['seatID']
        flag = msg['flag']
        cmd = {
            'id'    : 3004,
            'flag'  : flag
        }

        sendJson = json.dumps(cmd)
        sock = self.games[seatID].getSock()

        for s in sock:
            s.send(sendJson)

    def togetherRes(self, msg, owner, inputs):
        user = msg['user']
        addScore = msg['addScore']
        seatID = msg['seatID']
        self.games[seatID].clear()
        dbPath = "DB/test.db"
        cx = sqlite3.connect(dbPath)
        cu = cx.cursor()
        query = "select * from rtable where username = " + "'" + user + "'"
        cu.execute(query)
        res = cu.fetchall()
        print user
        print res
        rank = res[0][0] + addScore
        updateStr = "update rtable set rank = " + str(rank) + " where username = " + "'" + user + "'"
        cu.execute(updateStr)
        cx.commit()
        cx.close()
