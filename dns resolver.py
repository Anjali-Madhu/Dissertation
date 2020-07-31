
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
    host = str(input("Enter host name :"))
    type = int(input("Enter IP type(0 for ipv4,1 for ipv6) : "))
    #create and display DNS Queries
    if type == 0:
        d = DNSRecord.question(host,"A")
    else:
        d = DNSRecord.question(host,"AAAA")
    print("DNS query : \n",d)
    print()
    print("************************************************************************")
    count = -1
    dataframe = pd.DataFrame(columns=["Resolver","UDP reply","Time taken for UDP","HTTPS reply","Time taken for HTTPS","HTTPS time/UDP time"])
    for r in resolvers:
        
        count+=1
        value = resolvers[r]
        url = value[0]
        ip = value[1][0]
        #change the order in which the functions are invokes
        if count % 2==0:
            (reply_udp,time_udp) = dns_udp(d,ip)
            (reply_https,time_https) = dns_https(d,url)
            
            
        else:
            (reply_https,time_https) = dns_https(d,url)
            (reply_udp,time_udp) = dns_udp(d,ip)
          
            
        dataframe = dataframe.append({
                                    "Resolver":r,
                                    "UDP reply":reply_udp,
                                    "Time taken for UDP":time_udp,
                                    "HTTPS reply": reply_https,
                                    "Time taken for HTTPS":time_https,
                                    "HTTPS time/UDP time":time_https/time_udp},
                                    ignore_index=True)
       
   

    for index,row in dataframe.iterrows():
        if index >0:
            print("________________________________________________________________________")
        print()
        print(row["Resolver"])
        print("\nUDP  : \n")
        print(row["UDP reply"])
        print("\n HTTPS : \n")
        print(row["HTTPS reply"])
        print()
        
    print()    
    print("************************************************************************")
    print()   
    print(dataframe[['Resolver','Time taken for UDP','Time taken for HTTPS']])
    udp_mean = dataframe['Time taken for UDP'].mean()
    https_mean = dataframe['Time taken for HTTPS'].mean()
    udp_max = dataframe['Time taken for UDP'].max()
    https_max = dataframe['Time taken for HTTPS'].max()
    udp_min = dataframe['Time taken for UDP'].min()
    https_min = dataframe['Time taken for HTTPS'].min()
    print("UDP")
    print("Average : ",udp_mean)
    print("Minimum : ",udp_min)
    print("Maximum : ",udp_max)
    print("HTTPS")
    print("Average : ",https_mean)
    print("Minimum : ",https_min)
    print("Maximum : ",https_max)
    print()
    
    
  
if __name__ == "__main__":
    main()
            
        
            
            
    
    





