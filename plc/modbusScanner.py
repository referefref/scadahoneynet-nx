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
import string, socket,sys,time,binascii,re,struct

MP = 502
HOST = "127.0.0.1"

# Function codes: There are three sets of function codes defined
# by Modbus, public, user_defined and reserved.

# User defined(from Ethereal):

# read_coils(1),read_input_discretes(2),
# read_mult_regs(3),read_input_regs (4),write_coil(5),write_single_reg(6)
# ,read_except_stat(7),diagnostics(8),program_484(9),poll_484(10),
# get_comm_event_ctrs(11),get_comm_event_log(12), program_584_984(13)
# poll_584_984(14),force_mult_coils(15),write_mult_regs(16),report_slave_id(17)
# ,program_884_u84(18),reset_comm_link(19), read_genl_ref(20),
# write_genl_ref(21),mask_write_reg(22),read_write_reg(23),
# read_fifo_queue(24),program_ConCept(40),firmware_replace(25),
# program_584_984_2(126), report_local_addr_mb(127)

docFuncCodes = {'rc':'\x01', 'rdi':'\x02', 'rhr':'\x03', 'rir':'\x04', 'wsc':'\x05', 'wsr':'\x06', 'res':'\x07', 'd':'\x08', 'gcec':'\x0B', 'gcel':'\x0C', 'wmc':'\x0F', 'wmr':'\x10', 'rsid':'\x11', 'rfd':'\x14', 'wfd':'\x15','mwr':'x16','rwmd':'\x17','rfq':'\x18','eit':'\x2B'}

#There are two defined ranges of user-defined function codes, ie
#65 to 72 decimal (0x41 to 0x58), and 100 to 110 decimal (0x64 to 0x6E).
#The user can select and implement a function code without any
#approval from modbus.org. 

userFuncCodes={'65':'\x65','66':'\x66','66':'\x66','67':'\x67','68':'\x68','69':'\x69','70':'\x70','71':'\x71','72':'\x72','100':'\x100','101':'\x101','102':'\x102','103':'\x103','104':'\x104','105':'\x105','106':'\x106','107':'\x107','108':'\x108','109':'\x109','110':'\x110'}

# Modbus protocol exception codes
# illegal_function(0x01),illegal_address(0x02),illegal_value(0x03)
# illegal_response(0x04),acknowledge(0x05),slave_busy(0x06),
# negative_ack(0x07),memory_err(0x08),gateway_unavailable(0x0a),
# gateway_trgt_fail(0x0b)

errorCodes={'if':'\x01','ia':'\x02','iv':'\x03','ir':'\x04','a':'\x05','sb':'\x06','na':'\x07','me':'\x08','gu':'\x0a','gtf':'\x0b'}

# Default values for various headers
transID = '\x00\x00'
protoID = '\x00\x00'

unitID = '\x01'
funcCode = '\x23'
refNum = '\x00\x00'
wordCount = '\x00\x03'
Data = '\x24\x30\x31\x43\x0d\x00'

bitCount = '\x00\x10'


modbusLen = '\x00\x0d'


## Define all types of headers here

# Lets call this Modbus TCP header
'''
struct modbus_tcp
{
      struct modbusTCP_hdr
      {
      __u16 transaction_id; (2 bytes)
      __u16 protocol_id; (2 bytes)
      __u16 length; (2 bytes)
      }modbus_h;


'''


# Lets call this Modbus header
'''
      struct modbus_hdr
      {
      __u8 unit_id; (1 byte)
      __u8 func_code; (1 byte)
      __u16 ref_num; (2 bytes)

      # This part or even the reference number can change for
      some Modbus packets
      __u16 word_cnt; (2 bytes) 
      __u8 byte_cnt; ( 1 byte)
      }modbus_d;
}
'''

modbusHdr=unitID+funcCode+refNum+bitCount

# len is number of bytes of modbusHdr together with all the data
# Modbus header is 6 bytes (transid:2 protoid:2 length:2), I think
# length is just the data part.
# modbusHdr=unitID+funcCode+refNum +'\xff\x00'

# modbusLen=hex(modbusHdr.__len__())


modbusLen = struct.pack('h',modbusHdr.__len__())
print modbusLen

#modbusLen = hex(modbusLen)
#print modbusLen
modbusTCPHdr = transID + protoID + modbusLen


#a=struct.pack('!h',6), to make integer 6 into \x00\x06
#len = struct.pack('!h',len)
#tcpHdr = transID+protID+len

# convert int len into hex use hex(len)
# For converting back, use int(hexstr,16)

totalLen = (modbusTCPHdr + modbusHdr).__len__()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, MP))

sendData = modbusTCPHdr + modbusHdr
charData = struct.unpack(totalLen*'b',sendData)
print totalLen, "\n", charData

s.send(sendData)
data=s.recv(65535)

datalen = data.__len__()
charData = struct.unpack(datalen*'b',data)

print charData
    
s.close()

'''
# Working scanner code
while 1:

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", MP))

    modbusHdr=unitID+funcCode+refNum+wordCnt

    try :
        s.settimeout(3)
        s.send(tcpHdr+modbusHdr)
        data=s.recv(65535)
        len=data.__len__()
        data=struct.unpack(len*'c ',data)
        print data
        s.close()
    except:
        s.close()
    
    intfc = ord(funcCode)
    intfc = intfc+1
    funcCode = struct.pack('b',intfc)

'''
