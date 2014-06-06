#!/usr/bin/python
#-*-coding:utf-8-*-
__author__ = 'gzs2482'

class game(object):
    def __init__(self, gid):
        self.gid = gid
        self.init(gid)

    def init(self, gid):
        self.id = gid
        self.left = False
        self.right = False
        self.leftUser = None
        self.rightUser = None
        self.leftSock = None
        self.rightSock = None
        self.players = 0
    def addPlayer(self, user, pos, sock):
        self.players += 1
        if pos == 2:
            self.right = True
            self.rightUser = user
            self.rightSock = sock

        elif pos == 1:
            self.left = True
            self.leftUser = user
            self.leftSock = sock

        return self.players

    def getSock(self):
        return [self.leftSock, self.rightSock]

    def clear(self):
        self.init(self.gid)