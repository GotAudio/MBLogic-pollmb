#!/usr/bin/python
##############################################################################
# Project: 	pollws
# Module: 	pollws.py
# Purpose: 	Command line modbus REST web service client (master).
# Language:	Python 2.5
# Date:		09-Apr-2008.
# Ver:		25-Feb-2009.
# Author:	M. Griffin.
# Copyright:	2008 - 2009 - Michael Griffin       <m.os.griffin@gmail.com>
#
# This file is part of pollws.
# pollws is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# pollws is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with pollws. If not, see <http://www.gnu.org/licenses/>.
#
# Important:	WHEN EDITING THIS FILE, USE TABS TO INDENT - NOT SPACES!
##############################################################################

import signal
import sys

import time

from mbprotocols import ModbusRestSimpleClient

import mbpollcommon

##############################################################################

# Signal handler.
def SigHandler(signum, frame):
	print('Polling terminated from keyboard at %s' % time.ctime())
	sys.exit(3)


# Initialise the signal handler.
signal.signal(signal.SIGINT, SigHandler)


############################################################

# Get the command line parameter options.
CmdOpts = mbpollcommon.GetOptions('web')

# timeout is ignored. It is present only to provide compatibility
# with pollmb, but it is not used here. 
host, port, timeout = CmdOpts.GetHost()

print('\nContacting MB-REST host at %s port %d' % (host, port))

mbclient = ModbusRestSimpleClient.ModbusRestSimpleClient(host, port)


############################################################

# Get what data to send.
SendUnitID, SendFunction, SendAddr, SendQty, SendData = CmdOpts.GetMBRequest()

# Preset the transaction ID.
SendTransID = 0


# If this is a write function, convert the data to an ASCII string format.
BinData = '0000'
try:
	if (SendFunction == 5):
		sendval = int(SendData)
		if sendval == 0:
			BinData = '0000'
		elif sendval == 1:
			BinData = 'FF00'
		else:
			print('Invalid data for Modbus function %d.' % SendFunction)
			sys.exit(4)
	elif (SendFunction == 15):
		BinData = SendData
	elif SendFunction in  (6, 16):
		BinData = SendData
	else:
		BinData = '0000'
except:
	print('Invalid data for Modbus function %d.' % SendFunction)
	sys.exit(4)


############################################################

# Get the polling rate info.
PollRepeats, PollDelay = CmdOpts.GetPollRate()

# Get whether to use "silent" polling.
PollSilently = CmdOpts.GetIsSilent()

# Record the starting time for reporting statistics.
StartTime = time.time()


# Tell the user what the program is going to do.
IntroStr = 'Sending Modbus func: %d, addr: %d, qty: %d, data: %s for %d polls at %d msec'
print(IntroStr % (SendFunction, SendAddr, SendQty, SendData, PollRepeats, int(PollDelay * 1000.0)))

# Poll the server.
for i in xrange(PollRepeats):

	# Increment the transaction ID.
	SendTransID += 1
	if (SendTransID > 65535):
		SendTransID = 0

	# Send the Modbus request message to the server.
	try:
		Recv_TransID, Recv_Function, Recv_Data, Recv_HttpStatus, Recv_HttpResult = \
			mbclient.SendRequest(SendTransID, SendUnitID, SendFunction, SendAddr, SendQty, MsgData = BinData)
	except:
		print('Error communicating with host.')
		sys.exit(5)


	# Decode the reply.
	hexdata = Recv_Data

	if not PollSilently:
		if (Recv_HttpStatus != 200):
			print('%d: Server Error Code: %s   Reason: %s' % (i + 1, Recv_HttpStatus, Recv_HttpResult))
		else:
			if (Recv_Function < 128):
				print('%d: Reply was: function: %d, data: %s' % (i + 1, Recv_Function, hexdata))
			else:
				print('%d: Reply was: Error: %d, Exception: %s' % (i + 1, Recv_Function, hexdata))

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


