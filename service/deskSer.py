#!/usr/bin/python
#-*-coding:utf-8-*-
__author__ = 'gzs2482'

class desk(object):
    def __init__(self):
        self.right = False
        self.left = False
        self.rName = None
        self.lName = None
        self.leftState = False
        self.rightState = False
        self.leftSock = None
        self.rightSock = None

    def sitDown(self, msg):
        if not self.right:
            self.right = True
            self.rName = msg['user']
            return 2

        if not self.left:
            self.left = True
            self.lName = msg['user']
            return 1

        return 0

    def standUp(self, pos):
        if pos == 2:
            self.right = False
        elif pos == 1:
            self.left = False

    def setState(self, pos, state):
        if pos == 2:
            self.rightState = state
        elif pos == 1:
            self.leftState = state

    def readyDesk(self):

        if self.leftState & self.rightState:
             return [self.leftSock, self.rightSock]
        else:
            return []

    def setSock(self, pos, owner):
        print pos, owner
        if pos == 2:
            self.rightSock = owner
        elif pos == 1:
            self.leftSock = owner

    def clear(self):
        self.leftState = False
        self.rightState = False