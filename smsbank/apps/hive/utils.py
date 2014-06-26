# encoding: utf-8
import SocketServer as ss
import socket
import string
import re
from __builtin__ import Exception
import multiprocessing as mp
import json
#import os
#import sys
import time
from time import sleep
import random


port = 44444
host = "0.0.0.0"

class LocalAPIServer(mp.Process):
    host = "0.0.0.0"
    port = 13666
    queue = None
    sender = None
    
    def __init__(self, queue, sender):
        mp.Process.__init__(self)
        #self.socket = socket
        self.queue = queue
        self.sender = sender
        
    def run(self):
        locaServer = ss.UDPServer((self.host, self.port), self.LocalAPIListener)
        locaServer.serve_forever()
        None
        
    class LocalAPIListener(ss.BaseRequestHandler):
        def handle(self):
            realCommand = json.loads(self.request[0])
            if realCommand['command'] in ['USSD', 'SMS']:
                realCommand['seed'] = random.randrange(10000, 20000)
            
            self.queue.put(realCommand)
            print "we got signal"
            print realCommand
            socket = self.request[1]
            socket.sendto(self.respond(realCommand), self.client_address)

            """
            id
            command
            data ->
                SMS -> recipient, message
                USSD -> code
                RAW -> command (debug command)
                
            """
        def respond(self, command):
            return "OK"

            


class GoipUDPSender(mp.Process):
    """
    """
    queue = None
    
    def __init__(self, queue):
        mp.Process.__init__(self)
        self.queue = queue
        #self.sendResponces()
        
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print "Colonel Sender is ready for Action!"
        while True:
            if not self.queue.empty():
                while not self.queue.empty():
                    data = self.queue.get()
                    print data['data']
                    sock.sendto(data['data'], data['host'])
            else:
                time.sleep(1)
                
    
  
class GoipUDPListener(ss.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """
    devPool = {}
    senderQueue = mp.Queue
    sender = None
    
    def handle(self):
        #data = self.request[0].strip()
        socket = self.request[1]
        #command = self.getCommand(self.request[0])
        query = self.parseRequest(self.request[0])
        print self.devPool
        self.queryDevice(query['id'], query['pass'])
        #device = self.devPool[query['id']]['device']
        
        
        # BAD Practice BUT, now we init event
        
        #if not apiQueue.empty():
        while not apiQueue.empty():
            outbound = apiQueue.get()
            if self.deviceActive(outbound['id']):
                if outbound['command'] == 'MSG':
                    outbound['command'] = 'SMSG'
                if outbound['command'] == 'USSD':
                    outbound['command'] = 'SUSSD'
                outQueue = self.outbound[query['id']]['queue']
                outQueue.put(outbound)
            #self.queryDevice(devId, passw, 1)
            None
        
        
        queue = self.devPool[query['id']]['queue']
        queue.put_nowait(query)
        print "queue " + str(queue.qsize())
        print "Process count: " + str(len(self.devPool))
    
    def queryDevice(self, devId, passw, auth=0):
        authState = True
        if auth == 1:
            authState = self.authDevice()
        if (not self.deviceActive(devId) and authState):
            queue = mp.Queue()
            #device = mp.Process(target=deviceWorker, args=(devId, self.client_address, queue, senderQueue))
            device = deviceWorker(devId, self.client_address, queue, senderQueue)
            device.start()
            #device._target.newRun()
            self.devPool[devId] = {}
            self.devPool[devId]['device'] = device
            self.devPool[devId]['queue'] = queue
        return device
    
    def deviceActive(self, devId):
        if devId in self.devPool:
            return True
        return False
  
    def getCommand(self, data):
        newdata = re.search('^([a-zA-Z]+)', data)
        return newdata.group(0)
        
    def parseRequest(self, data):
        reqdata = string.split(data, ";")
        command = {}
        if data['command'] in ['req', 'CGATT', 'CELLINFO', 'STATE', 'EXPIRY', 'RECIEVE']:
            for comBun in reqdata:
                if string.find(comBun, ":") != -1:
                    tmp = string.split(comBun,":")
                    if tmp[0] == 'password':    #correcting for Chinese protocol unevenness, when sometimes its 'pass' and sometimes its 'password' 
                        tmp[0] = 'pass'
                    command[tmp[0]] = tmp[1]
        elif data['command'] in ['MSG', 'USSD', 'PASSWORD', 'SEND', 'WAIT', 'DONE', 'OK']:
            command['id'] = data.split()[1]
            command['data'] = data
        command['command'] = self.getCommand(data)
        return command
        
    def authDevice(self, command, password):
        '''
        Must check existence of such device id in DB and check password afterwards
        '''
        if password == '123':
            return True
        return False

class deviceWorker(mp.Process):
    devid = None
    expire = int(20)
    cgatt = None
    imei = None
    num = None
    voipStatus = None
    voipState = None
    imsi = None
    iccid = None
    cells = None
    gsm = None
    signal = None
    expiryTime = None
    killFlag = False
    password = None
    
    host = None
    port = None
    
    queueIn = None
    queueOut = None
    
    def __init__(self, devid, host, queue, outQueue):
        mp.Process.__init__(self)
        self.devid = devid
        self.queueIn = queue
        self.host = host
        self.queueOut = outQueue 
        print host
        print "mein Konstruktor: " + str(self.devid)
        #self.newRun()
        
    
        
    def run(self):
        '''
        Main worker function
        '''
        print "OMG! I'm Running wild and free!"
        self.expire = 20
        while True:
            if not self.queueIn.empty():
                self.processRequest()
            else:
                sleep(1)
                self.expire -= 1
                print "Expire is now: " + str(self.expire)
                
            #if self.expire <= 0:
            #    print "For thy Emperor of the catkind I will sacrifice myself"
                #return
                #self.terminate()
            
    def processRequest(self):
        responce = {}
        responce['host'] = self.host
        while not self.queueIn.empty():
            data = self.queueIn.get_nowait()
            print data
            if data['command'] in ['req', 'CGATT', 'CELLINFO', 'STATE', 'EXPIRY']:
                responce['data'] = self.processServiceRequest(data)
                self.queueOut.put(responce)
            elif data['command'] in ['SMS', 'USSD']:
                responce['data'] = self.processOutbound(data)
            elif data['command'] in ['RECIEVE', ]:
                responce = self.processInboundSMS(data)
        
    def processOutbound(self, data):
        if not (data['id'] in self.msgActive):
            None  
        
    def processInboundSMS(self, data):
        """
        RECEIVE:1403245796;id:1;password:123;srcnum:+79520999249;msg:MSGBODY
        """
        print "I've got message from {}. It reads as follows:".data['srcnum']
        print data['msg']
        print "Technically I can save it, but I won't"
        responce = string.join(['RECIEVE', data['RECEIEVE'], 'OK'])
        print responce
        return responce
             

    def processServiceRequest(self, data):
        if data['command'] == 'req':
            responce = 'reg:' + str(data['req']) +';status:200'
            return responce
        #if not regActive(commandData["id"]):
        #    return
        
        if data['command'] == 'CGATT':
            self.cgatt = data['cgatt'] 
        elif data['command'] == 'CELLINFO':
            cells = string.split(data['info'].strip('"'), ",")
            print cells
            self.cells = cells
        elif data['command'] == 'STATE':
            None
        elif data['command'] == 'EXPIRY':
            self.expire = data['exp']
        else:
            raise Exception
            return
        responce = data['command'] + " " + str(data[data['command']]) + " OK"
        return responce

    
if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 44444
    senderQueue = mp.Queue()
    #sender  = mp.Process(target=GoipUDPSender, args=(senderQueue,))
    sender = GoipUDPSender(senderQueue,)
    sender.start()
    
    apiQueue = mp.Queue()
    apiHandle = LocalAPIServer(apiQueue, senderQueue)
    apiHandle.start()
    
    server = ss.UDPServer((HOST, PORT), GoipUDPListener)
    server.serve_forever()
