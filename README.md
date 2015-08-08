MBLogic-pollmb

Ken Selvia (kenselvia@gmail.com) August 6th, 2015

This branch contains minor modifications to Michael Griffin's Python pollmb.py component 
delivered as part of his larger suite of applications called MBLogic.

The original application is hosted on SourceForge here;

http://sourceforge.net/projects/mblogic/

Folder here was mbtools_2011-01-07.zip\pollmb in original source material.

I made changes to support the following command line options;

-f 65 : Added support for Omni Text register data types. Read function 65, write function 66 (9000-9999 Addresses)

-c y  : Convert output to ascii characters (useful for reading 8 byte ascii or text registers

-b y  : Brief mode which will not display header and other information. CSV output more easily manipulated


Examples (python must be installed in your path. I have Python 2.7);

C:\...\pollmb>pollmb -h 127.0.0.1 -f 3 -p 1502 -a 4114 -q 1 -c y -u 1 -b y -r 3

	-h Host:	127.0.0.1
	-f Function:	3 (read holding register)
	-p Port:	1502
	-a Address:4114
	-q Length:	1
	-c Output:	Convert to character (ASCII)
	-u UnitId:	1
	-b Brief:	Output CSV, do not show header

127.0.0.1, 4114, ABCDEFGH

C:\..\pollmb>pollmb -h 127.0.0.1 -f 3 -p 1502 -a 4114 -q 1 -c y -u 1 -b y -r 1000 -s y

Elapsed time was 1.021000 seconds.
A total of 1000 Registers were sent at a rate of 979.431789 Registers per second.


This change is released under terms of the GPL license as per Michaels original code;

 Project: 	pollmb

 Module: 	pollmb.py

 Purpose: 	Command line modbus client (master).

 Language:	Python 2.5

 Date:		01-Apr-2008.

 Ver:		24-Sep-2009.

 Author:	M. Griffin.

 Copyright:	2008 - 2009 - Michael Griffin       <m.os.griffin@gmail.com>



 This file is part of pollmb.

 pollmb is free software: you can redistribute it and/or modify

 it under the terms of the GNU General Public License as published by

 the Free Software Foundation, either version 3 of the License, or

 (at your option) any later version.

 pollmb is distributed in the hope that it will be useful,

 but WITHOUT ANY WARRANTY; without even the implied warranty of

 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the

 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License

 along with pollmb. If not, see <http://www.gnu.org/licenses/>.
