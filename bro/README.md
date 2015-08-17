# Bro EtherNet/IP Protocol Analyser #
This repository contains the necessary files in order to inspect Ethernet/IP
packets with Bro.

## Installation ##
Go to your Bro directory, then copy the files from the src/ and script/
directories into the same place, then compile Bro with:
    # ./configure && make && make install

Then you can run Bro with any of your .pcap files containing some Ethernet/IP
traffic with the following command:
    $ bro -r <file.pcap>
And then take a look at the .log files and more precisely the enip.log file.

## Things to do ##
-Add UDP keep-alive packets and non 44818 packets
-Add some tests (write the <test>.bro in /testing/btest/scripts/base/protocols/enip)
on precise .pcap captures (in /testing/btest/Traces/dnp3) and debug the protocol 
analyser if necessary,
-Find attacks on the EtherNet/IP protocol and a way to detect them,
-Add these functionalities into this Bro protocol analyser.

## Detect attacks ##
From http://reversemode.com/downloads/logix_report_basecamp.pdf
     Generic attacks
          0: Metasploit exploits such as STOP/CRASH CPU, RESET/CRASH ETHER (see ethernetip-multi.rb)
     	  1: Interface Configuration
	  2: Forcing a CPU Stop
     	  3: Crash CPU

     Specific to 1756-ENBT module
     	  4: Dump 1756-ENBT’s module boot code
	  5: Reset 1756-ENBT module
	  6: Crash 1756-ENBT module
	  7: Flash Update