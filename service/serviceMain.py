#!/usr/bin/python
#-*-coding:utf-8-*-
__author__ = 'gzs2482'

import socket
import select
from dispatcher import dispatcher
from login_service import login_service
from room_service import room_service
from game_service import game_service
import json

class serviceMain(object):
    def __init__(self):
        self.__configure()
        self.inputs = [self.server]
        self.__initDispatcher()
        self.run()

    def __configure(self):
        self.host = ''
        self.port = 2345
        self.bufsiz = 20480
        self.ADDR = (self.host, self.port)

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(False)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(self.ADDR)
        self.server.listen(10)

    def run(self):

        while True:
            print 'waiting for next connection'
            readable, writable , exceptional = select.select(self.inputs, [], [])

            for s in readable:
                if s is self.server:
                    connection, client_address = s.accept()
                    print 'connect from ', client_address
                    connection.setblocking(False)
                    self.inputs.append(connection)
                else:
                    try:
                        data = s.recv(self.bufsiz)
                        print 'receive data from client: ', data
                    except socket.error:
                        self.inputs.remove(s)
                    else:
                        msg = json.loads(data)
                        self.dispatcher.dispatch(msg, s)

    def __initDispatcher(self):
        self.dispatcher = dispatcher(self.inputs)
        self.loginSer = login_service()
        self.roomSer = room_service()
        self.gameSer = game_service()

        self.dispatcher.register(1000, self.loginSer)
        self.dispatcher.register(2000, self.roomSer)
        self.dispatcher.register(2001, self.roomSer)
        self.dispatcher.register(2002, self.roomSer)
        self.dispatcher.register(2003, self.roomSer)
        self.dispatcher.register(2004, self.roomSer)
        self.dispatcher.register(3000, self.gameSer)
        self.dispatcher.register(3001, self.gameSer)
        self.dispatcher.register(3002, self.gameSer)
        self.dispatcher.register(3003, self.gameSer)
        self.dispatcher.register(3004, self.gameSer)
        self.dispatcher.register(3005, self.gameSer)
    def __dispatch(self, msg, owner):
        self.dispatcher.dispatch(msg, owner)

