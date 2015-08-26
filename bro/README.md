# Bro EtherNet/IP Protocol Analyser #
This repository contains the necessary files in order to inspect Ethernet/IP
packets with Bro.

## Installation ##
You can download Bro at https://www.bro.org/.
Go to your Bro directory, then copy the files from the src/ testing/ and script/
directories into the same place, then compile Bro with:
    # ./configure && make && make install

## Usage ##
You can run Bro with any of your .pcap files containing some Ethernet/IP
traffic with the following command:
    $ bro -r <file.pcap> [<bro-script.bro>]
And then take a look at the .log files and more precisely the enip.log file.
You can also inspect live trafic from an interface using Broctl.

## TODO ##
-Add UDP keep-alive packets and non 44818 packets.
-Add some tests (write the <test>.bro in /testing/btest/scripts/base/protocols/enip)
on precise .pcap captures (in /testing/btest/Traces/dnp3) and debug the protocol 
analyser if necessary.
-Add a bash script to make the installation automatic.
-Add Bro in Minicps.
-Debug the following issues.

## Know issues ##
-Some packets are not parsed.
-The keep-alive packet on port 2222 without header are not parsed.
-There is a out_of_bound: RR_Unit:timeout exception on some packets.
-There is a out_of_bound: Data_Address:len exception on some packets.

## Detect attacks ##
From http://reversemode.com/downloads/logix_report_basecamp.pdf
     Generic attacks
     	  1: Interface Configuration

     Specific to 1756-ENBT module
     	  4: Dump 1756-ENBT’s module boot code
	  5: Reset 1756-ENBT module
	  6: Crash 1756-ENBT module
	  7: Flash Update