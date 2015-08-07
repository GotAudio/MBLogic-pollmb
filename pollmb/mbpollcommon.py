##############################################################################
# Project: 	mbpoll
# Module: 	mbpollcommon.py
# Purpose: 	Command line modbus client (master).
# Language:	Python 2.5
# Date:		01-Apr-2008.
# Ver:		25-Feb-2009.
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
"""
This library provides common functions to the pollmb and pollws programs.
"""

import getopt, sys

############################################################

_HelpIntroMBStr = """
This program provides a simple command line ModbusTCP client. It can be 
used to read or write to ModbusTCP servers. It can also be used to measure 
the performance of ModbusTCP servers by repeated polling them and measuring 
the elaspsed time. It supports Modbus functions 1, 2, 3, 4, 5, 6, 15, and 16.

It has a variety of command line parameters. Any parameters which are not 
specified will use their default values. These include:

Ethernet address:
-h Host name of the ModbusTCP server. The default is localhost.
-p Port number of the ModbusTCP server. The default is 502.
-t Receive time-out in seconds. The default is 60. The minimum is 1.
"""

_HelpIntroWSStr = """
This program provides a simple command line MB-REST web service client. 
It can be used to read or write to MB-REST http web servers. It can also 
be used to measure the performance of MB-REST http servers by repeated 
polling them and measuring the elaspsed time. It supports Modbus functions 
1, 2, 3, 4, 5, 6, 15, and 16.

It has a variety of command line parameters. Any parameters which are not 
specified will use their default values. These include:

URL address:
-h Host name of the Modbus REST web server (including the path). 
	The default is localhost.
-p Port number of the Modbus REST web server. The default is 80.
-t This is present for compatibility with pollmb, but is ignored here.
"""


_HelpMainStr = """

Modbus parameters:
-f Function. The default is 1.
-a Address (Modbus memory). The default is 0.
-q Quantity of addresses. The default is 1.
-u Unit ID. The default is 1

Polling parameters:
-r Repeats. Number of times to perform the poll. The default is 1.
-y Delay time between repeats in milliseconds. The default is 1.
-d Data to send to the server. Default is 0000.
-s Silent mode. 'Y' or 'y' will suppress displaying data. Default is 'no'.

Data:
For functions 1, 2, 3, or 4, any data specified is ignored. For functions 
5, 6, 15, or 16, data must be specified. For function 5 (write single coil),
data must be either 0 or 1. For function 15 (write multiple coils), data must 
be 0 and 1 characters, in multiples of 8 characters. E.g. 00111010.
For functions 6 and 16 (write single or multiple registers), data must be
in hexadecimal with 4 characters per register. Hexadecimal values a to f may
be in lower or upper case.

Return Codes:
The following command line return codes are defined:
0 = No errors.
2 = Bad command line.
3 = Program was terminated from keyboard.
4 = Invalid data for modbus function.
5 = Error communicating with host.
6 = Invalid modbus parameters

Polling performance measurement:
When used to measure polling performance, silent mode should be enabled.
When more than one repeat is specified, extra information is displayed
after polling is completed. This includes elapsed time, number of
data elements transfered, and the data transfer rate. When trying to measure
maximum speed a large enough number of polls should be specified to allow
measurement over several (e.g. 5 to 10) seconds in order to get an accurate 
reading.

"""

_HelpExampleMBStr = """
Example:
./pollmb.py -p 8502 -f 3 -a 0 -q 125 -y 0 -r 30000 -s y

Poll a server at port 8502 to read 125 holding registers starting at
address 0, and repeat 30000 times with a delay time of 0 while not displaying
the results of each poll.
"""

_HelpExampleWSStr = """
Example:
./pollws.py -h localhost/modbus -p 8080 -f 3 -a 0 -q 125 -y 0 -r 30000 -s y

Poll a server at port 8080 to read 125 holding registers starting at
address 0, and repeat 30000 times with a delay time of 0 while not displaying
the results of each poll.
"""

_HelpLicenseStr = """

Author: Michael Griffin
Copyright 2008 - 2009 Michael Griffin. This is free software. You may 
redistribute copies of it under the terms of the GNU General Public License
<http://www.gnu.org/licenses/gpl.html>. There is NO WARRANTY, to the
extent permitted by law.

"""

############################################################

# Construct the help string for pollmb.
HelpStrMB = _HelpIntroMBStr + _HelpMainStr + _HelpExampleMBStr + _HelpLicenseStr

# Construct the help string for pollws.
HelpStrWS = _HelpIntroWSStr + _HelpMainStr + _HelpExampleWSStr + _HelpLicenseStr

############################################################
# Get the command line options.
# These include the host and port numbers and the modbus
# function parameters. These may be set by the user on the command line. 
# If the user does not set any options, then default values are used.
#
class GetOptions:

	########################################################
	# hosttype (string) = The type of host. If this is 'web',
	# the default port will be set to 80 (for web service). 
	# For anything else, it will be be 502 (for ModbusTCP).
	# The help string will also be initialised according
	# to this same parameter.
	def __init__(self, hosttype):
		if (hosttype == 'web'):
			self._port = 80
			self._HelpStr = HelpStrWS
		else:
			self._port = 502
			self._HelpStr = HelpStrMB

		self._host = 'localhost'
		self._timeout = 60.0
		self._unitID = 1
		self._function = 1
		self._addr = 0
		self._qty = 1
		self._repeats = 1
		self._delay = 0.001
		self._data = '0000'
		self._silent = False

		# Read the command line options.
		try:
			opts, args = getopt.getopt(sys.argv[1:], 'p: h: t: f: a: q: u: r: y: d: s:', 
				['port', 'host', 'timeout', 'func', 'addr', 'qty', 'uid', 'repeat', 'delay', 'data', 'silent'])
		except:
			print('Unrecognised options.')
			sys.exit(2)

		# Check if no parameters specified. If none, then print out the help message.
		if (opts == []):
			print(self._HelpStr)
			sys.exit(2)


		# Parse out the options.
		for o, a in opts:
			if o == '-p':
				try:
					self._port = int(a)
				except:
					print('Invalid port number.')
					sys.exit(2)
			elif o == '-h':
				self._host = a

			elif o == '-t':
				try:
					self._timeout = float(a)
				except:
					print('Invalid time out value.')
					sys.exit(2)
				if (self._timeout < 1.0):
					print('Specified timeout is too small.')
					sys.exit(2)
			elif o == '-f':
				try:
					self._function = int(a)
				except:
					print('Invalid Modbus function.')
					sys.exit(2)
				if ((self._function < 0) or (self._function > 255)):
					print('Modbus function code is out of range.')
					sys.exit(2)
			elif o == '-a':
				try:
					self._addr = int(a)
				except:
					print('Invalid Modbus address.')
					sys.exit(2)
				if ((self._addr < 0) or (self._addr > 65536)):
					print('Modbus address is out of range.')
					sys.exit(2)
			elif o == '-q':
				try:
					self._qty = int(a)
				except:
					print('Invalid Modbus quantity.')
					sys.exit(2)
				if ((self._qty < 0) or (self._qty > 65536)):
					print('Modbus quantity is out of range.')
					sys.exit(2)
			elif o == '-u':
				try:
					self._unitID = int(a)
				except:
					print('Invalid Modbus Unit ID.')
					sys.exit(2)
				if ((self._unitID < 0) or (self._unitID > 255)):
					print('Modbus Unit ID is out of range.')
					sys.exit(2)
			elif o == '-r':
				try:
					self._repeats = int(a)
				except:
					print('Invalid number of poll repeats.')
					sys.exit(2)
			elif o == '-y':
				try:
					self._delay = int(a)/1000.0
				except:
					print('Invalid repeat delay.')
					sys.exit(2)
			elif o == '-d':
				self._data = a
			elif o == '-s':
				self._silent = (a in ('y', 'Y'))
			else:
				print('Unrecognised option %s %s' % (o, a))
				sys.exit(2)

	########################################################
	# Return the host and port setting.
	def GetHost(self):
		return self._host, self._port, self._timeout

	########################################################
	# Return the Modbus function info.
	def GetMBRequest(self):
		return self._unitID, self._function, self._addr, self._qty, self._data

	########################################################
	# Return the polling rate information.
	def GetPollRate(self):
		return self._repeats, self._delay

	########################################################
	# Return whether polling should be "silent" (do not report
	# read or write results).
	def GetIsSilent(self):
		return self._silent

############################################################


# Report polling information if multiple polls were made.
# Parameters:
# ElapsedTime (float) = Elapsed time in seconds.
# SendQty (integer) = Amount of data sent per poll.
# PollRepeats (integer) = Number of polling cycles.
# SendFunction (integer) = Modbus function used.
def ReportStats(ElapsedTime, SendQty, PollRepeats, SendFunction):

	TotalSent = SendQty * PollRepeats
	AchievedRate =  TotalSent / ElapsedTime
	if (AchievedRate > 1000.0):
		AchievedRateStr = '%.0f' % AchievedRate
	else:
		AchievedRateStr = '%f' % AchievedRate

	if SendFunction in (1, 5, 15):
		PollType = 'Coils'
	elif SendFunction == 2:
		PollType = 'Inputs'
	else:
		PollType = 'Registers'

	print('\nElapsed time was %f seconds.' % ElapsedTime)
	print('A total of %d %s were sent at a rate of %s %s per second.\n' % (TotalSent, PollType, AchievedRateStr, PollType))

############################################################


