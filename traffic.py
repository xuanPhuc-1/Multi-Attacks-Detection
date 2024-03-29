import sys
import getopt
import time
from os import popen
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import sendp, IP, UDP, Ether, TCP
from random import randrange
import string
import random

def payload_generator(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def generateSourceIP(start, end):
    #not valid for first octet of IP address
    #not_valid = [10, 127, 254, 1, 2, 169, 172, 192]

    #selects a random number in the range [1,256)
    #first = randrange(1, 256)

    #while first in not_valid:
    #    first = randrange(1, 256)
    
    #eg, ip = "100.200.10.1"
    #ip = ".".join([str(first), str(randrange(1,256)), str(randrange(1,256)), str(randrange(1,256))])
    ip = ".".join([str(10), str(0), str(0), str(randrange(start,end))])

    return ip

#start, end: given as command line arguments. eg, python traffic.py -s 2 -e 65  
def generateDestinationIP(start, end):
    first = 10
    second = 0
    third = 0

    #eg, ip = "10.0.0.64"
    ip = ".".join([str(first), str(second), str(third), str(randrange(start,end))])

    return ip

def main(argv):
    #print argv
    
    #getopt.getopt() parses command line arguments and options 
    try:
        opts, args = getopt.getopt(sys.argv[1:], 's:e:', ['start=','end='])
    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt =='-s':
            start = int(arg)
        elif opt =='-e':
            end = int(arg)

    if start == '':
        sys.exit()
    if end == '':
        sys.exit()
    
    #open interface eth0 to send packets
    interface = popen('ifconfig | awk \'/eth0/ {print $1}\'').read()

    for i in range(100000):
        packets = Ether() / IP(dst = generateDestinationIP (start, end), src = generateSourceIP (start, end)) / UDP(dport = 80, sport = 2)/payload_generator(size=randrange(1,50))
        print(repr(packets))

	    #rstrip() strips whitespace characters from the end of interface
        sendp(packets, iface = interface.rstrip(), inter = 0.1)

if __name__ == '__main__': # 3000 packets normal
  main(sys.argv)
#   for i in range (1, 3):
#       main(sys.argv[0], sys.argv[1])
#       #time.sleep ()


