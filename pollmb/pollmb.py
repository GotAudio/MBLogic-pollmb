#!/usr/bin/python
##############################################################################
# Project: 	pollmb
# Module: 	pollmb.py
# Purpose: 	Command line modbus client (master).
# Language:	Python 2.5
# Date:		01-Apr-2008.
# Ver:		24-Sep-2009.
# Author:	M. Griffin.
# Copyright:	2008 - 2009 - Michael Griffin       <m.os.griffin@gmail.com>
#
# This file is part of pollmb.
# pollmb is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# pollmb is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with pollmb. If not, see <http://www.gnu.org/licenses/>.
#
# Important:	WHEN EDITING THIS FILE, USE TABS TO INDENT - NOT SPACES!
##############################################################################

import signal
import sys

import time

from mbprotocols import ModbusTCPSimpleClient
from mbprotocols import ModbusDataStrLib

import mbpollcommon

############################################################

# Signal handler.
def SigHandler(signum, frame):
	print('Polling terminated from keyboard at %s' % time.ctime())
	sys.exit(3)


# Initialise the signal handler.
signal.signal(signal.SIGINT, SigHandler)


############################################################

# Get the command line parameter options.
CmdOpts = mbpollcommon.GetOptions('modbustcp')

BriefOutput = CmdOpts.GetBrief()

host, port, timeout = CmdOpts.GetHost()

if not BriefOutput:
	print('\nContacting Modbus host at %s port %d timeout %.01f sec.' % (host, port, timeout))

try:
	mbclient = ModbusTCPSimpleClient.ModbusTCPSimpleClient(host, port, timeout)
except:
	if not BriefOutput:
		print('Failed to contact host.')
	else:
		print('%s, %d, Failed to contact host.' % (host, port))
	sys.exit(5)



############################################################

# Get what data to send.
SendUnitID, SendFunction, CharAddr, SendQty, SendData = CmdOpts.GetMBRequest()

SendAddr = int(CharAddr)

# Preset the transaction ID.
SendTransID = 0

CharacterOutput = CmdOpts.GetCharacter()


# If this is a write function, convert the data to binary packed string format.
BinData = '\x00\x00'
try:
	if (SendFunction == 5):
		sendval = int(SendData)
		if sendval in (0, 1):
			BinData = ModbusDataStrLib.coilvalue(int(SendData))
		else:
			print('Invalid data for Modbus Function %d.' % SendFunction)
			sys.exit(4)
	elif (SendFunction == 15):
		BinData = ModbusDataStrLib.bininversor(SendData)
	elif SendFunction in  (6, 16, 66):
		BinData = ModbusDataStrLib.hex2bin(SendData)
	elif SendFunction == 65:
		BinData = '\x00\x00'
	else:
		BinData = '\x00\x00'
except:
	print('Invalid data for modbus function %d.' % SendFunction)
	sys.exit(4)

# Construct the Modbus request message.
try:
	RequestMsg = mbclient.MakeRawRequest(SendTransID, SendUnitID, SendFunction, SendAddr, SendQty, MsgData = BinData)
except:
	RequestMsg = ''

if (RequestMsg == ''):
	print('Invalid ModbuS parameters.')
	sys.exit(6)

############################################################

# Get the polling rate info.
PollRepeats, PollDelay = CmdOpts.GetPollRate()

# Get whether to use "silent" polling.
PollSilently = CmdOpts.GetIsSilent()

# Record the starting time for reporting statistics.
StartTime = time.time()


# Tell the user what the program is going to do.
IntroStr = 'Sending Modbus function: %d, addr: %d, qty: %d, data: %s for %d polls at %d msec'
if not BriefOutput:
	print(IntroStr % (SendFunction, SendAddr, SendQty, SendData, PollRepeats, int(PollDelay * 1000.0)))

# Poll the server.
for i in xrange(PollRepeats):

	# Send the Modbus request message to the server.
	try:
		mbclient.SendRawRequest(RequestMsg)
	except:
		if not BriefOutput:
			print('Error sending request to host.')
		else:
			print('%s, %d, Error sending request to host.' % (host, port))
		sys.exit(5)

	# Get the reply.
	try:
		Recv_TransID, Recv_Function, Recv_Data = mbclient.ReceiveResponse()
	except:
		if not BriefOutput:
			print('Error receiving data from host.')
		else:
			print('%s, %d, Error receiving data from host.' % (host, port))
		sys.exit(5)

	# Decode the reply.
	try:
		if CharacterOutput:
			hexdata = str(Recv_Data)
		elif Recv_Function in (1, 2):
			hexdata = ModbusDataStrLib.inversorbin(Recv_Data)
		elif Recv_Function in (3, 4):
			hexdata = ModbusDataStrLib.bin2hex(Recv_Data)
		elif  Recv_Function in (5, 6, 15, 16):
			hexdata = ModbusDataStrLib.bin2hex(Recv_Data)
		elif Recv_Function == 65:
			hexdata = ModbusDataStrLib.bin2hex(Recv_Data)
#[104:106] + '.' + ModbusDataStrLib.bin2hex(Recv_Data)[106:108] + '.' + ModbusDataStrLib.bin2hex(Recv_Data)[108:110] + '.' + ModbusDataStrLib.bin2hex(Recv_Data)[110:112]
		elif (Recv_Function > 127):
			hexdata = str(Recv_Data)
		else:
			hexdata = 'No Data'
	except:
		if not BriefOutput:
			print('Bad data format received from host for function %d' % Recv_Function)
		else:
			print('%s, %d, Bad data format received from host for function %d' % (host, port, Recv_Function))
		sys.exit(5)

	if not PollSilently:
		if not BriefOutput:
			print('%d: Reply was: function: %d, data: %s' % (i + 1, Recv_Function, hexdata))
		else:
			print('%s, %d, %s' % (host, SendAddr, hexdata))


	# Delay until the next scheduled polling time.
	if (i < (PollRepeats - 1)):
		time.sleep(PollDelay)


############################################################

# Report polling information if multiple polls were made.
if (PollRepeats > 1):
	EndTime = time.time()
	ElapsedTime = EndTime - StartTime
	mbpollcommon.ReportStats(ElapsedTime, SendQty, PollRepeats, SendFunction)


############################################################


