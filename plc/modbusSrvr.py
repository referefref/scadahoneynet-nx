# This  program is free software; you may redistribute and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; Version 2.
# This guarantees your right to use, modify, and redistribute
# this software under certain conditions This program is distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details at http://www.gnu.org/copyleft/gpl.html .
# The authors or our employer, will not be liable for any direct,
# indirect, special or consequential damages from the use of or
# failure to use of improper use of this tool.
# (Version 0.1, Venkat Pothamsetty, vpothams@cisco.com)


#! /usr/bin/python2

import string, socket, struct, thread, os
from modbusHdrs import *
from struct import *
from time import gmtime, strftime

# Response comes from the source port 502, so all the packets
# that this scripts gets should be queries which are destinated
# to port 502.

HOST = "127.0.0.1"
ModbusPort = 502

class modbusSrvr:
    
    # Default class values, will fillup when we receive the packet,
    # This class variable method may not work if threaded.
    transID = '\x00\x00'
    protoID = '\x00\x00'
    
    # We need to fill this length while sending the packet
    modbusLen = '\x00'
    
    unitID = '\x00'
    funcCode = '\x00'
    refNum = '\x00\x00'
    wordCount = '\x00\x00'
    bitCount = '\x00\x00'
    
    # Data, the length will be different too
    Data = '\x00\x00'
    dataLen = '\x00'

    modbusTCPHdr = transID+protoID
    modbusHdr=unitID+funcCode

    logFile = "/var/log/scadahoneynet.log"

    def listen(self):
        data = '\x00'
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((HOST, ModbusPort))
            s.listen(1)
        except socket.error, msg:
            self.writeLog("Socket Error: %s" %(msg))

        while 1:
            conn, addr = s.accept()
            self.writeLog("Got a connect from %s from port %d" %(addr[0],addr[1]))
            self.modbusConn = conn            
            thread.start_new_thread(self.handleConnection, (data,conn))


    def handleConnection(self, data,conn):
         while 1:

            try:
                data = conn.recv(512)

                # Send control to implementCommands from here
                self.processData(data,conn)

            except socket.error, msg:
                conn.close()
                self.writeLog("Socket Error: %s" %(msg))
                break
            
    def processData(self, data,conn):

        datalen = data.__len__()
        self.dataLen = hex(datalen)
        headers1 = struct.unpack(datalen*'b',data)
        #print headers1

        datalen = datalen - 8 # Removing the 'hhhb' part 
        
        # It always has transID(2 bytes), protoID(2bytes), len(2bytes)
        # unitID(1 byte) and funcID (1byte)
        headers = struct.unpack('hhhbb'+datalen*'b',data)
        #print headers
        
        # Build your datastructure
        self.transID = headers[0]
        self.protoID = headers[1]
        self.modbusLen = headers[2]

        self.unitID = headers[3]
        self.funcCode = headers[4]

        self.writeLog("Got functionCode:%d\n" %(self.funcCode))
        
        self.sendResponse(data,conn,self.funcCode)
            

    def sendResponse(self,data,conn,code):

        # read_coils(1),read_input_discretes(2),
        # read_mult_regs(3),read_input_regs (4),write_coil(5),
        # read_except_stat(7),diagnostics(8),write_single_reg(6)
        # ,read_except_stat(7),diagnostics(8),program_484(9),
        # poll_484(10), get_comm_event_ctrs(11),get_comm_event_log(12),
        # program_584_984(13), poll_584_984(14),force_mult_coils(15),
        # write_mult_regs(16),report_slave_id(17)
        # ,program_884_u84(18),reset_comm_link(19), read_genl_ref(20),
        # write_genl_ref(21),mask_write_reg(22),read_write_reg(23),
        # read_fifo_queue(24),program_ConCept(40),firmware_replace(25),
        # program_584_984_2(126), report_local_addr_mb(127)
        
        if(code == 1):
            # Read coils response
            # The query has a refnum and a bitcount (say 16) the
            # response has a bytecount (of therefore 8) and the
            # corresponding sized data
            templen = int(self.dataLen,16)
            
            # This is specific for funcID 1
            headers = struct.unpack('!hhhbbhh'+(templen-12)*'b',data)

           
            self.refNum = headers[5]
            self.bitCount = headers[6]

            Data = (self.bitCount/8)*'\x00'
            byteCount = self.bitCount/8


            temphdr = struct.pack('BBB',self.unitID, self.funcCode, byteCount)
            packetLen = temphdr.__len__() + byteCount
            #print "here 2", packetLen, byteCount

            #Packet length screwed up
            rcr = struct.pack('hhhBBhh',self.transID, self.protoID, packetLen, self.unitID,self.funcCode,self.refNum,byteCount)
            
            conn.send(rcr+Data)
            

        elif(code == 3):
            # Read multiple registers response
            # The query has a word count of 24. The answer came in with data
            # of 48 bytes with bytecount with data as all zeros. Some times
            # the response is multiple encapsulated Modbus packets, need to
            # understand what response is when

            self.writeLog("Multiple registers response")
            
        elif(code == 4):
            self.writeLog("Sending read_input_regs response")
            
        elif(code == 8):
            # Diagnostics
            #print "Diagnostics"
            dg = modbusTCPhdr + modbusHdr + Data
            
            
        elif(code == 16):
            # # Write multiple registers response, it is the same as the
            # query packet with out the data, so we need to take the
            # query packet, strip the data and send it again.
            # The query has refnum, wordCount and byteCount.  The response
            # has just wordCount.  In the query packet, the next
            # heaers after functioncde are refNum and wordCount
            # headers = struct.unpack('hhhbb'+datalen*'b',data)
            
            templen = int(self.dataLen,16)
            
            # This is specific for funcID 16
            headers = struct.unpack('!hhhbbhh'+(templen-12)*'b',data)

            
            self.refNum = headers[5]
            self.wordCount = headers[6]

            #print self.transID
            #print self.protoID
            
            #print self.refNum
            #print self.wordCount

            temphdr = struct.pack('bbhh',self.unitID, self.funcCode,self.refNum, self.wordCount)
            packetLen = temphdr.__len__()


            wmr = struct.pack('hhhbbhh',self.transID, self.protoID, packetLen, self.unitID,self.funcCode,self.refNum,self.wordCount)
            
            conn.send(wmr)

        else:

            # Send unknown exception function code
            templen = int(self.dataLen,16)
            
            templen=templen-8
            
            # This is specific for modbusTCPHdr + ModbusHdr
            headers = struct.unpack('!hhhBB'+templen*'b',data)
            
            self.funcCode = headers[4]

            self.writeLog("Got a Modbus Query, Function Code%d" %(self.funcCode))
            self.writeLog("Sending an unknown functioncode exception")
                        
            illegalFunc = ord('\x01')
            
            self.funcCode = self.funcCode + ord('\x80')

            temphdr = struct.pack('BBB',self.unitID, self.funcCode, illegalFunc)
            packetLen = temphdr.__len__()


            funcException = struct.pack('hhhBBB',self.transID, self.protoID, packetLen, self.unitID,self.funcCode,illegalFunc)
            
            conn.send(funcException)

    def writeLog(self,string):    
        fileobject = open(self.logFile, 'a')
        fileobject.write("Scadahoneynet, Modbus simulation Log" +":"+(time.strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) +":"+ string +"\n"))
        fileobject.close()
    

    def main(self):
        
        self.listen()

modbusSrvr().main()

