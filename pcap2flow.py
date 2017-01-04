from scapy.all import *
from scapy.layers import http
from scapy.error import Scapy_Exception
import os
import sys
import threading
import signal
import md5



def get_http_headers(raw_payload):
    try:
        headers_raw = raw_payload[:raw_payload.index("\r\n\r\n")+2]
        headers = dict(re.findall(r'(?P<name>.*?):(?P<value>.*?)\r\n', headers_raw))
    except:
        return None
    if 'Content-Type' not in headers:
        return None
    return headers

def http_assembler(PCAP):
    carved_images, faces_detected = 0, 0
    p = rdpcap(PCAP)
    sessions = p.sessions();
    session_count=0;

    response_hashes={};

    for session in sessions:
        print('\nSession...'+ str(session_count));
        session_count = session_count + 1;

        raw_payload = ''
        for packet in sessions[session]:
            #if str(packet[TCP].payload).find('GET'):
            #    print('FOUND'+ str(packet[TCP].dport));
            try:
                if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                    raw_payload += str(packet[TCP].payload)
            except:
                pass
            #print http_request stuff
            if packet.haslayer(http.HTTPRequest):
                http_layer = packet.getlayer(http.HTTPRequest)
                ip_layer = packet.getlayer(IP)
                print('- Request from {0[src]} {1[Method]} {1[Host]}{1[Path]}'.format(ip_layer.fields, http_layer.fields));
            elif packet.haslayer(http.HTTPResponse):
                http_layer = packet.getlayer(http.HTTPResponse);
                if 'Content-Encoding' in http_layer.fields:
                    content_encoding = http_layer.fields['Content-Encoding'].strip();
                    data = packet[Raw].load;
                    if content_encoding == 'gzip':
                        data = zlib.decompress(data, 16)
                    elif headers['Content-Encoding'] == 'deflate':
                        data = zlib.decompress(data)

                    headers_raw = raw_payload[:raw_payload.index("\r\n\r\n")+2]
                    print("- Response:"+ headers_raw);
                    print("- Response-data:"+ data);

                    #response_hashes[md5.new(data).hexdigest()] = md5.new(data).hexdigest();

        #print("unique responses:"+response_hashes);
    return

pcap_file='/Users/edgecrush3r/Downloads/misc1000_traffic.pcap';
print('Loading pcap '+ pcap_file);
http_assembler(pcap_file);
