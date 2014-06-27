# encoding: utf-8
import SocketServer as ss
import string
import re
from __builtin__ import Exception
import multiprocessing as mp
import json
from time import sleep
import random

port = 44444
host = "0.0.0.0"
devPassword = "123"
defaultRandomNumber = 4

class LocalAPIServer(mp.Process):
    host = "0.0.0.0"
    port = 13666
    queue = None
    sender = None

    def __init__(self, queue):
        mp.Process.__init__(self)
        #self.socket = socket
        self.queue = queue
        #self.sender = sender

    def run(self):
        locaServer = self.QueuedServer((self.host, self.port), self.LocalAPIListener)
        locaServer.queue = self.queue
        #self.LocalAPIListener.getQueue(self.queue)
        locaServer.serve_forever()
        None

    class LocalAPIListener(ss.BaseRequestHandler):
        queue = None

        def __init__(self, request, client_address, server):
            ss.BaseRequestHandler.__init__(self, request, client_address, server)
            #self.queue = queue

        def handle(self):
            realCommand = json.loads(self.request[0])
            if realCommand['command'] in ['USSD', 'SMS']:
                realCommand['seed'] = random.randrange(200000, 299999)
                #realCommand['seed'] = "2236910"
                #realCommand['data']['message'] = "MSGBODY"

            #LocalAPIServer.queue.put(realCommand)
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

        def getQueue(self, queue):
            self.queue = queue

    class QueuedServer(ss.UDPServer):
        queue = None

        def finish_request(self, request, client_address):
            #self.RequestHandlerClass(self, request, client_address, self.queue )
            #print self.queue.__class__
            self.RequestHandlerClass.queue = self.queue
            ss.UDPServer.finish_request(self, request, client_address)



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
        sock = self.request[1]
        #socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #command = self.getCommand(self.request[0])


        query = self.parseRequest(self.request[0])
        print query
        if query['command'] == 'RECEIVE':
            print self.request[0]
        if 'id' not in query:
            query['id'] = seedDic[int(self.request[0].split()[1])]
            query['pass'] = devPassword                         #MUST CHECK source and compare it with actual device data
        print query
        #print self.devPool
        self.queryDevice(query['id'], query['pass'])
        #device = self.devPool[query['id']]['device']
        if not senderQueue.empty():
            while not senderQueue.empty():
                data = senderQueue.get()
                print data['host']
                print data['data']
                sock.sendto(data['data'], data['host'])

        # BAD Practice BUT, now we init event

        #if not apiQueue.empty():
        #print apiQueue
        while not apiQueue.empty():
            outbound = apiQueue.get()
            if self.deviceActive(outbound['id']):
                if outbound['command'] == 'SMS':
                    outbound['command'] = 'SMSG'
                if outbound['command'] == 'USSD':
                    outbound['command'] = 'SUSSD'
                print self.devPool[query['id']]['queue']
                outQueue = self.devPool[query['id']]['queue']
                outQueue.put(outbound)
            #self.queryDevice(devId, passw, 1)
            None


        queue = self.devPool[query['id']]['queue']
        queue.put_nowait(query)
        print "queue " + str(queue.qsize())
        print "Process count: " + str(len(self.devPool))

    def queryDevice(self, devId, passw, auth=0):
        authState = True
        # TODO: get or create device via DB
        # if auth == 1:
        #     authState = self.authDevice()
        if (not self.deviceActive(devId) and authState):
            queue = mp.Queue()
            #device = mp.Process(target=deviceWorker, args=(devId, self.client_address, queue, senderQueue))
            device = deviceWorker(devId, self.client_address, queue, senderQueue, seedDic)
            device.start()
            #device._target.newRun()
            self.devPool[devId] = {}
            self.devPool[devId]['device'] = device
            self.devPool[devId]['queue'] = queue
        return self.devPool[devId]['device']

    def deviceActive(self, devId):
        if str(devId) in self.devPool:
            return True
        return False

    def getCommand(self, data):
        newdata = re.search('^([a-zA-Z]+)', data)
        return newdata.group(0)

    def parseRequest(self, data):
        reqdata = string.split(data, ";")
        command = {}
        command['command'] = self.getCommand(data)
        #print command
        if command['command'] in ['req', 'CGATT', 'CELLINFO', 'STATE', 'EXPIRY', 'RECEIVE', 'DELIVER']:
            for comBun in reqdata:
                if string.find(comBun, ":") != -1:
                    tmp = string.split(comBun,":")
                    if tmp[0] == 'password':    #correcting for Chinese protocol unevenness, when sometimes its 'pass' and sometimes its 'password'
                        tmp[0] = 'pass'
                    command[tmp[0]] = tmp[1]
        elif command['command'] in ['MSG', 'USSD', 'PASSWORD', 'SEND', 'WAIT', 'DONE', 'OK']:
            command['seed'] = data.split()[1]
            command['data'] = data

        return command

    def authDevice(self, command, password):
        '''
        Must check existence of such device id in DB and check password afterwards
        '''
        # TODO: w
        if password == devPassword:
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

    msgActive = {}
    msgCount = 0
    msgSeeds = None

    host = None
    port = None

    queueIn = None
    queueOut = None

    def __init__(self, devid, host, queue, outQueue, seedArray):
        mp.Process.__init__(self)
        self.devid = devid
        self.queueIn = queue
        self.host = host
        self.queueOut = outQueue
        self.msgSeeds = seedArray

        self.state = {'new':        1,
                      'auth':       2,
                      'send':       3,
                      'waiting':    4,
                      'sent':       5,
                      'done':       6,
                      'delivered':  7,
                      }
        #print host
        #print "mein Konstruktor: " + str(self.devid)
        #self.newRun()



    def run(self):
        '''
        Main worker function
        '''
        #print "OMG! I'm Running wild and free!"
        #self.expire = 20
        while True:
            if not self.queueIn.empty():
                self.processRequest()
                self.msgActive['goipId'] = {}
            else:
                sleep(1)
                #self.expire -= 1
                #print "Expire is now: " + str(self.expire)

            #if self.expire <= 0:
            #    print "For thy Emperor of the catkind I will sacrifice myself"
                #return
                #self.terminate()

    def processRequest(self):
        response = {}
        response['host'] = self.host
        while not self.queueIn.empty():
            data = self.queueIn.get()
            #print data
            if data['command'] in ['req', 'CGATT', 'CELLINFO', 'STATE', 'EXPIRY']:
                response['data'] = self.processServiceRequest(data)
                self.queueOut.put(response)
            elif data['command'] in ['MSG', 'USSD', 'PASSWORD', 'SEND', 'WAIT', 'DONE', 'OK', 'SMSG', 'SUSSD', 'DELIVER']:
                response['data'] = self.processOutbound(data)
                self.queueOut.put(response)
            elif data['command'] in ['RECEIVE', ]:
                response['data'] = self.processInboundSMS(data)
                self.queueOut.put(response)
            else:
                raise Exception

            print response

    def processOutbound(self, data):
        if data['command'] == 'SMSG':
            self.msgCount += 1
            self.msgActive[data['seed']] = {}
            self.msgActive[data['seed']]['locId'] = self.msgCount
            self.msgIdIntersectionCheck(data['seed'])
            message = self.msgActive[data['seed']]
            self.msgSeeds[data['seed']] = self.devid

        if data['command'] == 'DELIVER':
            return "DELIVER OK" #not implemented
        data['seed'] = int(data['seed'])

        if not (int(data['seed']) in self.msgActive) or data['command'] == "DELIVER":
            return
        elif data['seed'] in self.msgActive:
            message = self.msgActive[data['seed']]

        if data['command'] == 'SMSG':
            message['state'] = self.state['new']
            message['message'] = data['data']['message']
            message['recipient'] = data['data']['recipient']
            response = " ".join(["MSG", str(data['seed']), str(len(data['data']['message'])), str(data['data']['message'])])
        elif data['command'] == 'PASSWORD':
            message['state'] = self.state['auth']
            response = " ".join([data['command'], str(data['seed']), devPassword])
        elif data['command'] == 'SEND':
            message['state'] = self.state['send']
            response = " ".join([data['command'], str(data['seed']), message['locId'], message['recipient']])
        elif data['command'] == 'WAIT':
            message['state'] = self.state['waiting']
            response = "WAIT OK"
            #response = " ".join(["OK", str(data['seed']), devPassword, message['recipient']])
        elif data['command'] == 'OK':
            goipId = data['data'].split()[3]
            self.msgActive['goipId'][goipId] = message
            message['state'] = self.state['sent']
            response = " ".join(["DONE", str(data['seed'])])
        elif data['command'] == 'DONE':
            # TODO: save outbound sms to database
            message['state'] = self.state['sent']
            del self.msgSeeds[data['seed']]
        elif data['command'] == 'DELIVER':
            message = self.msgActive['goipId'][data['sms_no']]
            message['state'] = self.state['delivered']
            response = data['command'] + " " + str(data[data['command']]) + " OK"



        return response


    def msgIdIntersectionCheck(self, msgId):
        while msgId in self.msgActive:
            msgId = random.randrange(2000000, 2999999)

    def processInboundSMS(self, data):
        """
        RECEIVE:1403245796;id:1;password:123;srcnum:+79520999249;msg:MSGBODY
        """
        print data
        print "I've got message from {}. It reads as follows:".format(data['srcnum'])
        print data['msg']
        print "Technically I can save it, but I won't"
        # TODO: save SMS to database
        response = " ".join(['RECEIVE', data['RECEIVE'], 'OK'])
        print response
        return response


    def processServiceRequest(self, data):
        if data['command'] == 'req':
            response = 'reg:' + str(data['req']) +';status:200'
            return response
        #if not regActive(commandData["id"]):
        #    return

        if data['command'] == 'CGATT':
            self.cgatt = data['cgatt']
        elif data['command'] == 'CELLINFO':
            cells = string.split(data['info'].strip('"'), ",")
            self.cells = cells
        elif data['command'] == 'STATE':
            None
        elif data['command'] == 'EXPIRY':
            self.expire = data['exp']
        else:
            raise Exception
            return
        response = data['command'] + " " + str(data[data['command']]) + " OK"
        return response


    '''
if __name__ == "__main__":
    pass
    HOST, PORT = "0.0.0.0", 44444
    senderQueue = mp.Queue()
    #sender  = mp.Process(target=GoipUDPSender, args=(senderQueue,))
    #sender = GoipUDPSender(senderQueue,)
    #sender.start()
    #senderSocket = None

    apiQueue = mp.Queue()
    apiHandle = LocalAPIServer(apiQueue,)
    apiHandle.start()
    manager = mp.Manager()
    seedDic = manager.dict()
    #listSock = mp.Value(typecode_or_type)

    #sleep(5)

    server = ss.UDPServer((HOST, PORT), GoipUDPListener)
    server.serve_forever()
    '''
