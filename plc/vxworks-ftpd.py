
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

import socket,re,string,time,thread


PORT = 21

HOST = "127.0.0.1"

ListCommandResponse = "150 Opening BINARY mode data connection\ndrwx------  1 user          2048 bin\ndrwx------  1 user          2048 usr\ndrwx------  1 user          2048 opt\ndrwx------  1 user          2048 \ndrwx------  1 user          2048 wwwroot\ndrwx------  1 user          2048 ftp\n"

SystResponse = "215 UNIX Type: VxWorks\r\n"

UnKnownResponse = "Unknown Command, Closing Connection \r\n"
CWD = "root"
                 
class vxworksFTPD:

    PORTport = "NULL"
    FTPConn = "NULL"
    ClientAddr = "NULL"
    logFile = "/var/log/scadahoneynet.log"
    
    # Bind the script to 21 and listen
    def listen(self):

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((HOST, PORT))
        except socket.error, msg:
            self.writeLog("Socket Error: %s" %(msg))

        while 1:
            s.listen(1)
            conn, addr = s.accept()
            self.ClientAddr = addr 
            self.writeLog("Got a connect from %s from port %d" %(addr[0],addr[1]))
            self.FTPConn = conn

            # Create a thread to handle each client
            thread.start_new_thread(self.handleConnection,(conn,1))


    # This is a wrapper which gets data from te connection and
    # passes them on to implementCommands for sending responses
    def handleConnection(self,conn,i):

        # The server sends 220 ready
        conn.send('220 FTP server (VxWorks version 2.6) ready.\r\n')
        
        while 1:

            try:
                data = conn.recv(512)

                # Send control to implementCommands from here
                self.implementCommands(data,conn)

            except socket.error, msg:
                conn.close()
                self.writeLog("Socket Error: %s" %(msg))
                break
        

    # Sees the command and builds a response
    def implementCommands(self,data,conn):
        # print "in implementCommands"
        
        # If the client sends USER command
        if(re.compile('user', re.IGNORECASE).search(data)):

            self.writeLog("Got a user command")
            conn.send('331 Guest login ok, send your complete e-mail address as a password.\r\n') #Send Login OK, which means the client will ask the user for
            return
        
        elif (re.compile('pass', re.IGNORECASE).search(data)):#Password

            self.writeLog("Got the password")
            # The client will send the PASS command next
            conn.send('230 User Logged in\r\n')# The command says the the username and password are OK
            return

        elif (re.compile('list', re.IGNORECASE).search(data)):#Password

            self.writeLog("Got a list command")

            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind((HOST,20))
                s.connect((self.ClientAddr[0],self.PORTport))

            except socket.error, msg:
                self.writeLog("Socket Error(list): %s" %(msg))

            # Need to handle exceptions for binding again and again
            self.FTPConn.send('150 Opening BINARY mode data connection\r\n')
            
            s.send(ListCommandResponse)
            s.close()
            
            self.FTPConn.send('226 Transfer Complete \r\n')

            #conn.send('250 Changed directory \r\n')# The command says the the username and password are OK
            return


        elif (re.compile('cwd', re.IGNORECASE).search(data)):#Password
            self.writeLog("Got a cwd command")
            f=string.splitfields(data,' ')
            directory = f[1]
            conn.send('250 Changed directory %s \r\n' %(directory))# The command says the the username and password are OK
            return

        elif (re.compile('port', re.IGNORECASE).search(data)):#Password
            
            conn.send('200 Port set OK\r\n') #After this you need to connect back to the port and listen for a command.  Convert each of the last numbers to hex and combine the two hexnumbers, convert the combined hex number to decimal and you should get the port number.#m,n=(hex(int(f[4])),hex(int(f[5]))

            f=string.splitfields(data,',')
            m,n=(hex(int(f[4])),hex(int(f[5])))
            x,y = (string.splitfields(m,'x'),string.splitfields(n,'x'))
            s='0x'+x[1]+y[1]
            port = int(s,16)
            self.PORTport = port
            return
            
        elif (re.compile('quit', re.IGNORECASE).search(data)):#QUIT
            self.writeLog("Got a QUIT command")
            conn.close()
            return

        elif (re.compile('retr', re.IGNORECASE).search(data)):#QUIT
            self.writeLog("Got RETR command")

            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind((HOST,20))
                s.connect((self.ClientAddr[0],self.PORTport))
            except socket.error, msg:
                self.writeLog("Socket Error(retr): %s" %(msg))

            self.FTPConn.send('150 Opening BINARY mode data connection\r\n')
            
            s.send('Hello, world file \r\n')
            s.close()

            self.FTPConn.send('226 Transfer Complete \r\n')

            return
        
        elif (re.compile('syst', re.IGNORECASE).search(data)):
            self.writeLog("Got a syst command")
            conn.send(SystResponse)
            return
            
        else:
            self.writeLog("Got a unkown command:%s" %(data))
            conn.send(UnKnownResponse)
            conn.close()
            return
        
    def writeLog(self,string):    
        fileobject = open(self.logFile, 'a')
        fileobject.write("Scadahoneynet, FTP Log" +":"+(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()) +":"+ string +"\n"))
        fileobject.close()

    def main(self):
        self.listen()

vxworksFTPD().main()
