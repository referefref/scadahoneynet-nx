
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


#! /usr/bin/python

import socket,re,string,thread,time

PORT = 23

HOST = "127.0.0.1"

CommandLine = 'Hostname#'

HelpResponse = "help                           Print this list\nioHelp                         Print I/O utilities help info\ndbgHelp                        Print debugger help info\nnfsHelp                        Print nfs help info\nnetHelp                        Print network help info\nspyHelp                        Print task histogrammer help info\ntimexHelp                      Print execution timer help info\nh         [n]                  Print (or set) shell history\ni         [task]               Summary of tasks' TCBs\nti        task                 Complete info on TCB for task\nsp        adr,args...          Spawn a task, pri=100, opt=0, stk=20000\ntaskSpawn name,pri,opt,stk,adr,args... Spawn a task\ntd        task                 Delete a task\nts        task                 Suspend a task\n"


class vxworksTelnetd:

    PORTport = "NULL"
    TelnetConn = "NULL"
    PWD = ""
    logFile = "/var/log/scadahoneynet.log"
    
    def listen(self):

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((HOST, PORT))
        except socket.error, msg:
            self.writeLog("Socket Error: %s" %(msg))
            
        while 1:
            s.listen(1)
            conn, addr = s.accept()
            
            self.writeLog("Got a connect from %s from port %d" %(addr[0],addr[1]))
            self.TelnetConn = conn
            thread.start_new_thread(self.handleConnection,(conn,1))

    # This is a wrapper which gets data from te connection and
    # passes them on to implementCommands for sending responses
    def handleConnection(self,conn,i):
        conn.sendall('VxWorks Login:')
        loginName = conn.recv(512)
        self.writeLog("Loginname:%s" %(loginName))
        conn.sendall('Password:')
        Password = conn.recv(512)
        self.writeLog("Password:%s" %(Password))
        
        while 1:
            # Shell command
            try:
                conn.sendall("%s" %(CommandLine))
                data = conn.recv(512)
                # Send control to implementCommands from here
                self.implementCommands(data,conn)
            except socket.error, msg:
                conn.close()
                self.writeLog("Socket Error: %s" %(msg))
                break


    def implementCommands(self,data,conn):

        if(re.compile('ls', re.IGNORECASE).search(data)):
            self.writeLog("Got a ls command")
            conn.send('-rw-r--r--    1 root     root           33 Mar  5 18:06 gw\r\n') 
        
        elif (re.compile('cd', re.IGNORECASE).search(data)):#Password
            self.writeLog("Got a cd command")
            f=string.splitfields(data,' ')
            PWD = f[1]
            return
        

        else:
            conn.send(HelpResponse)
            self.writeLog("Got a RET or unkknown command")
            #conn.send('Shell: Command not found\r\n')
            return

    def writeLog(self,string):    
        fileobject = open(self.logFile, 'a')
        fileobject.write("Scadahoneynet, Telnet Log" +":"+(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()) +":"+ string +"\n"))
        fileobject.close()
        
    def main(self):
        self.listen()

vxworksTelnetd().main()
