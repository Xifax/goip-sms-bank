# encoding: utf-8
import SocketServer as ss
import socket
import string
import re
from __builtin__ import Exception
import multiprocessing as mp
import os
import sys
from time import sleep

port = 44444
host = "0.0.0.0"

#commQueue = mp.A
class GoipUDPSender(mp.Process):
    """
    """
    socket = None
    queue = None
    
    def __init__(self, queue):
        self.socket = socket
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
        print self.devPool
        if not self.deviceActive(query['id']):
            if self.authDevice(query['id'], query['pass']):
                queue = mp.Queue()
                #device = mp.Process(target=deviceWorker, args=(query['id'], self.client_address, queue, senderQueue))
                device = deviceWorker(query['id'], self.client_address, queue, senderQueue)
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
                
            if self.expire <= 0:
                print "For thy Emperor of the catkind i will sacrifice myself"
                #return
                #self.terminate()
            
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
    
    server = ss.UDPServer((HOST, PORT), GoipUDPListener)
    server.serve_forever()
