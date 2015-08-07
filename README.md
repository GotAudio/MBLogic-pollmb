MBLogic-pollmb

Contains minor modifications to Michael Griffin's pollmb.py component 
delivered as part of his larger suite of applications called MBLogic.

The original application is hosted on SourceForge here;

http://sourceforge.net/projects/mblogic/

In the version here, I made changes to support the following command line options;

-f 65 : Added support for Omni Text register data types. Read function 65, write function 66 (9000-9999 Addresses)
-c y  : Convert output to ascii characters (useful for reading 8 byte ascii or text registers
-b y  : Brief mode which will not display header and other information. CSV output more easily manipulated
-r n  : Repeat command n times
-d n  : delay between reads when -r switch is present
-s y  : output only elapsed time and reads per second summary