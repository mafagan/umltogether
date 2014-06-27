#!/usr/bin/python
#-*-coding:utf-8-*-
from service import service
from deskSer import desk
import json
__author__ = 'gzs2482'

class room_service(service):
    def __init__(self):
        service.__init__(self)
        commands = {
            2000 : self.roomChat,
            2001 : self.roomSitDown,
            2002 : self.roomStandUp,
            2003 : self.getAllDesk,
            2004 : self.roomReadyState
        }
        self.registers(commands)
        self.initDesk()
        self.deskState = {}

    def roomSitDown(self, msg, owner, inputs):
        res = self.desks[msg['activityID']].sitDown(msg)
        if res == 0:
            return

        self.desks[msg['activityID']].setSock(res, owner)
        self.desks[msg['activityID']].setState(res, False)

        cmd = {
            'id'        : 2001,
            'activityID'    : msg['activityID'],
            'pos'       : res,
            'user'      : msg['user'],
            'standFlag' : False
        }

        if msg['user'] in  self.deskState.keys():
            cmdd = {
                'activityID'    : self.deskState[msg['user']][0],
                'pos'       : self.deskState[msg['user']][1]
            }
            cmd['standFlag'] = True
            cmd['UPID'] = self.deskState[msg['user']][0]
            cmd['UPpos'] = self.deskState[msg['user']][1]
            self.roomStandUp(cmdd, owner, inputs)

        self.deskState[msg['user']] = [msg['activityID'], res]



        sendJson = json.dumps(cmd)
        length = len(inputs)
        #print 'sockets: ', inputs
        for s in range(1, length):
            inputs[s].send(sendJson)

    def roomStandUp(self, msg, owner, inputs):
        seatID = msg['seatID']
        pos = msg['pos']
        self.desks[seatID].standUp(pos)
        self.desks[seatID].setState(pos, False)
        self.desks[seatID].setState(pos, False)
        self.desks[seatID].setSock(pos, None)


    def getAllDesk(self, msg, owner, inputs):
        cmd = {
            'id'    : 2003,
            'seatID': [],
            'pos'   : []
        }

        for i in range(16):
            if self.desks[i].right:
                cmd['seatID'].append(i)
                cmd['pos'].append(2)

            if self.desks[i].left:
                cmd['seatID'].append(i)
                cmd['pos'].append(1)
        sendJson = json.dumps(cmd)
        owner.send(sendJson)

    def initDesk(self):
        self.desks = []
        for i in range(16):
            self.desks.append(desk())

    def roomChat(self, msg, owner, inputs):
        text = '<p><b>[' + msg['user'] + ' said]:' + '</b></p></ br>' + '  ' + msg['text']
        cmd = {
            'id'    : 2000,
            'text'  : text
        }

        sendJson = json.dumps(cmd)
        length = len(inputs)

        for s in range(1, length):
            inputs[s].send(sendJson)


    def roomReadyState(self, msg, owner, inputs):
        state = msg['state']
        seatID = msg['seatID']
        pos = msg['pos']
        #print pos
        self.desks[seatID].setState(pos, state)
        cmd = {
            'id'    : 2004,
            'state' : state,
            'pos'   : pos,
            'gFlag' : False
        }

        deskState = self.desks[seatID].readyDesk()
        if len(deskState) == 0:
            sendJson = json.dumps(cmd)
            owner.send(sendJson)
            return

        if len(deskState) == 2:
            self.desks[seatID].clear()
            cmd['gFlag'] = True
            sendJson = json.dumps(cmd)
            for s in deskState:
                s.send(sendJson)
            return
