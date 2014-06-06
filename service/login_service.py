#!/usr/bin/python
#-*-coding:utf-8-*-
from service import service
import sqlite3
import json
__author__ = 'Winterma'

class login_service(service):
    def __init__(self):
        service.__init__(self)
        commands = {
            1000 : self.handle_login
        }
        self.registers(commands)

    def handle_login(self, msg, owner, inputs):
        user = msg['user']
        passwd = msg['passwd']

        dbPath = "DB/test.db"
        cx = sqlite3.connect(dbPath)
        cu = cx.cursor()
        cu.execute('CREATE TABLE if not exists user(passwd varchar(100), username VARCHAR(100) UNIQUE)')
        cx.commit()
        cu.execute('CREATE TABLE if not exists rtable(rank integer, username VARCHAR(100) UNIQUE)')
        cx.commit()

        cu.execute("select * from user where username = " + "'" + user + "'")

        res = cu.fetchall()
        print res
        sendData = {'id':1000}
        if len(res) == 0:
            insertStr = "insert into user values(" + "'" + passwd + "'," + "'" + user + "')"
            cu.execute(insertStr)
            cx.commit()

            creatRank = "insert into rtable values("  + str(0) + "," + "'" + user + "')"
            cu.execute(creatRank)
            cx.commit()
            sendData['loginFlag'] = True
        elif res[0][0] != passwd:
            sendData['loginFlag'] = False
        else:
            sendData['loginFlag'] = True

        if sendData['loginFlag']:
            queryStr = "select * from rtable order by rank desc limit 10"
            cu.execute(queryStr)
            res = cu.fetchall()
            sendData['rank'] = res
        sendJson = json.dumps(sendData)
        print 'send data to client: ',sendJson
        owner.send(sendJson)
        cx.close()