# encoding: utf-8
import SocketServer as ss
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
    '''
    '''
    
class GoipUDPListener(ss.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """
    devPool = {}

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        command = self.getCommand(self.request[0])
        query = self.parseRequest(self.request[0])
        if not self.deviceActive(query['id']):
            if self.authDevice(query['id'], query['pass']):
                #device = mp.Process(target=deviceWorker, args=(query['id'],))
                device = deviceWorker(query['id'])
                device.start()
                device.run()
                self.devPool[query['id']] = device
        device = self.devPool[query['id']]
        device._target.queueIn.put_nowait(query)
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
                
        return command
        
    def authDevice(self, command, password):
        '''
        Must check existence of such device id in DB and check password afterwards
        '''
        #Pseudocode:
        #dev = getDeviceById(id)
        #if command['id'] == dev.devId:
        #    if command['pass'] == dev.pass:
        #        return True
        #return False
        if password == '123':
            return True
        return False

class deviceWorker(mp.Process):
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
    
    queueIn = mp.Queue()
    queueOut = mp.Queue()
    
    def __init__(self, devid):
        mp.Process.__init__(self)
        self.devid = devid
        self.queueIn = mp.Queue()
        self.queueOut = mp.Queue()
        print "mein Konstruktor: " + str(self.devid)
        #return True
        
    def run(self):
        '''
        Main worker function
        '''
        print "OMG! I'm Running wild and free!"
        while True:
            if not self.queueIn.empty():
                self.processRequest()
            else:
                sleep(1)
            if self.killFlag:
                return
            
    def processRequest(self):
        data = self.queueIn.get_nowait()
        #self.queueIn.put_nowait(obj)
        #command = self.parseRequest(data)
        
    '''   
    def parseRequest(self, data):
        reqdata = string.split(data, ";")
        command = {}
        for comBun in reqdata:
            if string.find(comBun, ":") != -1:
                tmp = string.split(comBun,":")
                command[tmp[0]] = tmp[1]
        return command
    '''
    
if __name__ == "__main__":
    '''
    worker = deviceWorker(1)
    worker.queueIn.put_nowait("req:1")
    
    mp.Process(target=deviceWorker, args=(1,))
    '''
    HOST, PORT = "0.0.0.0", 44444
    server = ss.UDPServer((HOST, PORT), GoipUDPListener)
    server.serve_forever()
