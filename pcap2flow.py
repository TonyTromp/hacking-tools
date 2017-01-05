from scapy.all import *
from scapy.layers import http
from scapy.error import Scapy_Exception
import os
import sys
import threading
import signal
import md5
import urllib2;

def follow_http_streams(pcap_filename):
    p = rdpcap(pcap_filename)
    sessions = p.sessions();
    http_streams = {};
    for session in sessions:
        #first_packet=sessions[session][0];
        raw_payload = '';
        for packet in sessions[session]:
            key = '';
            if packet.haslayer(http.HTTPRequest):
                #print('Request: '+ str(packet[TCP].time) +' '+ str(packet[TCP].sport));
                key = str(packet[TCP].sport);
                if key in http_streams.keys():
                    http_streams[key] = { 'Request': packet[http.HTTPRequest],'Response': http_streams[key]['Response'] }
                else:
                    http_streams[key] = { 'Request': packet[http.HTTPRequest] }


            if packet.haslayer(http.HTTPResponse):
                #print('Response: '+ str(packet[TCP].time) +' '+ str(packet[TCP].dport));
                key = str(packet[TCP].dport);
                if key in http_streams.keys():
                    http_streams[key] = {'Request': http_streams[key]['Request'], 'Response': packet[http.HTTPResponse] }
                else:
                    http_streams[key] = {'Response': packet[http.HTTPResponse] }

    return http_streams;


#get http response (body) as text and deflate if content-encoding is set
def get_response_body(http_response):
    data = '';
    if 'Content-Encoding' in http_response.fields:
        content_encoding = http_response.fields['Content-Encoding'].strip();
        data = http_response[Raw].load;
        if content_encoding == 'gzip':
            data = zlib.decompress(data, 16)
        elif content_encoding == 'deflate':
            data = zlib.decompress(data);

    return data;

pcap_filename='/Users/edgecrush3r/Downloads/misc1000_traffic.pcap';
print('Loading pcap '+ pcap_filename);

# Build follow_http_stream
http_streams=follow_http_streams(pcap_filename);
# shift to sorted tuples
for k in sorted(http_streams.keys()):
    response      = http_streams[k]['Response'];
    response_text =  get_response_body(response);
    # if response contains :) print originating request
    if ':)' in response_text:
        request = http_streams[k]['Request'];
        print( k+' '+ urllib2.unquote( request.fields['Host'] +' '+ request.fields['Method'] +' '+  request.fields['Path'] ) );
