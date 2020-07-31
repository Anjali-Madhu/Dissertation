
import time
import requests
import socket
from dnslib import *
import sys
import pandas as pd

#list of resolvers
resolvers ={"CLOUDFARE":['https://cloudflare-dns.com/dns-query',['1.1.1.1']],
        "GOOGLE":['https://dns.google/dns-query',['8.8.8.8']],
        "operdns":['https://doh.opendns.com/dns-query',['208.67.222.222']],
        "quad9":['https://dns.quad9.net/dns-query',['9.9.9.9']]
        }

#function for dns over udp
def dns_udp(dns_query,ip):
    
    resolver_ip = (ip,53)
    #create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    then = time.time()
    
    #sent udp packet
    sent = sock.sendto(dns_query.pack(), resolver_ip)
    

    # Receive response
    data, server = sock.recvfrom(4096)
    now = time.time()
    return (DNSRecord.parse(data),now-then)

 #function for dns over HTTPS   
def dns_https(dns_query,url):
    
    params = {
     #'scheme':'dns',
     'dns':base64.urlsafe_b64encode(dns_query.pack()).replace(b"=",b"")
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
    
    #reply from the resolver
    now = time.time()
    return (DNSRecord.parse(ae.content),now-then)
    
 
def main():
#create and display DNS Queries for ipv4 and ipv6
    d = DNSRecord.question("google.com","A")
    d6 = DNSRecord.question("google.com","AAAA")
    print("DNS query ipv4 : \n",d)
    print("\nDNS query ipv6: \n",d6)
    print("************************************************************************")
    count = -1
    dataframe = pd.DataFrame(columns=["Resolver","UDP reply","Time taken for UDP","HTTPS reply","Time taken for HTTPS"])
    for r in resolvers:
        
        count+=1
        value = resolvers[r]
        url = value[0]
        ip = value[1][0]
        #change the order in which the functions are invokes
        if count % 2==0:
            (reply_udp,time_udp) = dns_udp(d,ip)
            (reply_udp6,time_udp6) = dns_udp(d6,ip)
            (reply_https,time_https) = dns_https(d,url)
            (reply_https6,time_https6) = dns_https(d6,url)
            
        else:
            (reply_https,time_https) = dns_https(d,url)
            (reply_https6,time_https) = dns_https(d6,url)
            (reply_udp,time_udp) = dns_udp(d,ip)
            (reply_udp6,time_udp6) = dns_udp(d6,ip)
            
        dataframe = dataframe.append({
                                    "Resolver":r+" ipv4",
                                    "UDP reply":reply_udp,
                                    "Time taken for UDP":time_udp,
                                    "HTTPS reply": reply_https,
                                    "Time taken for HTTPS":time_https},
                                    ignore_index=True)
        dataframe = dataframe.append({
                                    "Resolver":r+" ipv6",
                                    "UDP reply":reply_udp6,
                                    "Time taken for UDP":time_udp6,
                                    "HTTPS reply": reply_https6,
                                    "Time taken for HTTPS":time_https6},
                                    ignore_index=True)
    print()   
    print(dataframe[['Resolver','Time taken for UDP','Time taken for HTTPS']])
    print()
    print("************************************************************************")
    print()
    for index,row in dataframe.iterrows():
        print(row["Resolver"])
        print("\nUDP  : \n")
        print(row["UDP reply"])
        print("\n HTTPS : \n")
        print(row["HTTPS reply"])
        print("________________________________________________________________________")
        
    
        
if __name__ == "__main__":
    main()
            
        
            
            
    
    





