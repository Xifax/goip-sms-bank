# encoding: utf-8
import SocketServer as ss
import socket
import string
#import threading
import re
from __builtin__ import Exception
import multiprocessing as mp
import os
import sys
from time import sleep
#from _ast import Del

port = 44444
host = "0.0.0.0"

#commQueue = mp.A
class GoipUDPSender:
    """
    """
    socket = None
    queue = None
    
    def __init__(self, queue):
        self.socket = socket
        self.queue = queue
        self.sendResponces()
        
    def sendResponces(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print "Colonel Listener is ready for Action!"
        while True:
            if not self.queue.empty():
                while not self.queue.empty():
                    data = self.queue.get()
                    print data
                    sock.sendto(data['data'], data['host'])
            else:
                sleep(1)
                
    
  
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
        data = self.request[0].strip()
        socket = self.request[1]
        command = self.getCommand(self.request[0])
        query = self.parseRequest(self.request[0])
        if not self.deviceActive(query['id']):
            if self.authDevice(query['id'], query['pass']):
                queue = mp.Queue()
                device = mp.Process(target=deviceWorker, args=(query['id'], self.client_address, queue, senderQueue))
                #device = deviceWorker(query['id'])
                device.start()
                #device._target.newRun()
                self.devPool[query['id']] = {}
                self.devPool[query['id']]['device'] = device
                self.devPool[query['id']]['queue'] = queue
        device = self.devPool[query['id']]['device']
        queue = self.devPool[query['id']]['queue']
        queue.put_nowait(query)
        print "queue " + str(queue.qsize())
        print "Process count: " + str(len(self.devPool))
        
            
        #print "{} wrote:".format(self.client_address[0])
        #print data
        #command = self.getCommand(data)
        #print command
        responce = ''
        '''
        if command in ['req', 'CGATT', 'CELLINFO', 'STATE', 'EXPIRY']:
            responce = processServiceRequest(command, data)
        #print "I answered"
        #print responce
        '''
        #socket.sendto(responce, self.client_address)
    
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
        for comBun in reqdata:
            if string.find(comBun, ":") != -1:
                tmp = string.split(comBun,":")
                if tmp[0] == 'password':    #correcting for Chinese protocol unevenness, when sometimes its 'pass' and sometimes its 'password' 
                    tmp[0] = 'pass'
                command[tmp[0]] = tmp[1]
        command['command'] = self.getCommand(data)         
        return command
        
    def authDevice(self, command, password):
        '''
        Must check existence of such device id in DB and check password afterwards
        '''
        if password == '123':
            return True
        return False

class deviceWorker:
    devid = None
    expire = None
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
#        mp.Process.__init__(self)
        self.devid = devid
        self.queueIn = queue
        self.host = host
        self.queueOut = outQueue 
        print host
        #self.queueOut = mp.Queue()
        print "mein Konstruktor: " + str(self.devid)
        self.newRun()
        #return True
        
    def newRun(self):
        '''
        Main worker function
        '''
        print "OMG! I'm Running wild and free!"
        while True:
            if not self.queueIn.empty():
                self.processRequest()
            else:
                sleep(1)
            print "from ps queue size is " + str(self.queueIn.qsize())
            #if self.killFlag:
            #    return
            
    def processRequest(self):
        responce = {}
        while not self.queueIn.empty():
            data = self.queueIn.get_nowait()
            print data
            if data['command'] in ['req', 'CGATT', 'CELLINFO', 'STATE', 'EXPIRY']:
                responce['data'] = self.processServiceRequest(data)
                responce['host'] = self.host
                self.queueOut.put(responce)
                

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
            #self.stateWrite(commandData)
            None
            #print "Muich state"
        elif data['command'] == 'EXPIRY':
            #self.expiryWrite(commandData)
            #print "Much expiry"
            self.expire = data['exp']
        else:
            raise Exception
            return
        responce = data['command'] + " " + str(data[data['command']]) + " OK"
        return responce

    
if __name__ == "__main__":
    '''
    worker = deviceWorker(1)
    worker.queueIn.put_nowait("req:1")
    
    mp.Process(target=deviceWorker, args=(1,))
    '''
    HOST, PORT = "0.0.0.0", 44444
    senderQueue = mp.Queue()
    sender  = mp.Process(target=GoipUDPSender, args=(senderQueue,))
    sender.start()
    
    server = ss.UDPServer((HOST, PORT), GoipUDPListener)
    server.serve_forever()
