#!/usr/bin/python
#-*-coding:utf-8-*-
__author__ = 'gzs2482'

import socket
from time import ctime, sleep
import sqlite3
import os
import select
import Queue
import cx_Freeze.util
from service.serviceMain import serviceMain

ser = serviceMain()

'''
host = ''
port = 23456
bufsiz = 1024
ADDR = (host, port)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)
server.listen(10)

inputs = [server]
outputs = []
message_queues = {}

while inputs:
    sleep(0.01)
    print('waiting for next Client')
    readable, writable , exceptional = select.select(inputs, outputs, inputs)
    #print('server wait')
    print readable
    print writable

    for s in readable:

        if s is server:

            connection, client_address = s.accept()

            print 'connection from', client_address
            connection.setblocking(False)
            inputs.append(connection)
            message_queues[connection] = Queue.Queue()
        else:
            try:
                data = s.recv(21000)
            except socket.error:
                #s.close()
                inputs.remove(s)
                continue

            if data:
                print 'received ', data, ' from ', s.getpeername()
                message_queues[s].put(data)
                if s not in outputs:
                    outputs.append(s)

            else:
                print 'closing ', s.getpeername()
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()

    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except Queue.Empty:
            print s.getpeername(), ' queue empty'
            outputs.remove(s)
        else:
            print 'sending ', next_msg, ' to ', s.getpeername()
            s.send(next_msg)


    for s in exceptional:
        print ' exception condition on ', s.getpeername()

        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        del message_queues[s]



#socket.setdefaulttimeout(1)

tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSerSock.setblocking(False)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)


connection = []
try:
    while True:

        print('wait for connection')
        tcpSerSock, addr = tcpSerSock.accept()
        print('...connect from ', addr)
        connection.append([tcpSerSock, addr])


        for i in connection:
            data = i[0].recv(bufsiz)
            if not data:
                continue
            i[0].send('[%s] %s' % (ctime(), data))

        while True:
            data = tcpSerSock.recv(bufsiz)

            if not data:
                tcpSerSock.close()
                break
            tcpSerSock.send('[%s] %s' % (ctime(), data))

except BaseException, e:
    #print(e)
    tcpSerSock.close()

'''

'''
path = "E:\\test.db"
print(path)
cx = sqlite3.connect(path)
cu = cx.cursor()
#cu.execute('create table user(id integer primary key, passwd integer, username varchar(100) UNIQUE)')
#cu.execute("insert into user values(0, 123, 'winter')")
#cx.commit()
cu.execute("select * from user")
print(cu.fetchall())
'''