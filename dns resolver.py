# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 12:20:49 2020

@author: anjali
"""


import time
import requests
import socket
from dnslib import *
import sys
#create DNS Query
d = DNSRecord.question("google.com","A")

print(d)

#list of resolvers
resolvers ={"CLOUDFARE":['https://cloudflare-dns.com/dns-query',['1.1.1.1']],
        "GOOGLE":['https://dns.google/dns-query',['8.8.8.8']],
        "operdns":['https://doh.opendns.com/dns-query',['208.67.222.222']],
        "quad9":['https://dns.quad9.net/dns-query',['9.9.9.9']]
        }
        

for r in resolvers:
    print()
    print(r)
    print()
    print()
    print("DoH")
    
    value = resolvers[r]
    url = value[0]
    params = {
     #'scheme':'dns',
     'dns':d.pack()
     }
    headers = {
            'scheme':'https',
            'ct': 'application/dns-message',
            'accept':'application/dns-message',
            'cl':'33'
            }
    then = time.time()
    #send DNS request
    ae = requests.get(url,headers=headers,params=params)
    print("sent")
    #reply from the resolver
    print(ae)
    print(ae.content)
    now = time.time()
    
   
    print("time taken : ",now-then)
    print()
    print("UDP")
    
    server_address = (value[1][0],53)
    #create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = d.pack()
    print("query size :",sys.getsizeof(message))
    then = time.time()
    #sent udp packet
    sent = sock.sendto(message, server_address)
    print("sent")

    # Receive response
    
    data, server = sock.recvfrom(4096)
    print("SIze:",sys.getsizeof(data))
    now = time.time()
    print(DNSRecord.parse(data))
    print("time taken : ",now-then)
    print("__________________________________________________________________")
    
    





