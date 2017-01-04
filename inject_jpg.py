#!/usr/local/bin/python

#file
SRC_FILE='original.jpg';
DST_FILE='inject.jpg';

class SegmentMark(object):
  SegmentTypes = [
      { 'id':'SOI','byte': b'\xD8' ,'desc': 'start of image'}
    , { 'id':'EOI','byte': b'\xD9' ,'desc': 'end of image'}
    , { 'id':'COM','byte': b'\xFE' ,'desc': 'comment'}
    , { 'id':'SOS','byte': b'\xDA' ,'desc': 'start scan'}
    , { 'id':'SOF0','byte': b'\xC0' ,'desc': 'start of frame (baseline DCT)'}
    , { 'id':'SOF2','byte': b'\xC2' ,'desc': 'start of frame (progressive DCT)'}
    , { 'id':'DHT','byte': b'\xC4' ,'desc': 'Define Huffman Table'}
    , { 'id':'DQT','byte': b'\xDB' ,'desc': 'Define Quantization Table'}
    , { 'id':'APP1','byte': b'\xE1' ,'desc': 'APP1'}
    , { 'id':'APP2','byte': b'\xE2' ,'desc': 'APP2'}
  ];
  Type = None;
  # The following types are used
  # SOI - Start Of Image
  # EOI - End Of Image
  value = None;
  Bytes = None;

  def __new__(class_,SegmentType=None):
    class_.stype=SegmentType;
    return True;

  @staticmethod
  def GetSegmentType(byte=None):
    for i in range(len(SegmentMark.SegmentTypes)):
      if (SegmentMark.SegmentTypes[i]['byte']==byte):
	 return SegmentMark.SegmentTypes[i];
    return None;


class switch(object):
  value = None
  def __new__(class_, value):
      class_.value = value
      return True

def case(*args):
    return any((arg == switch.value for arg in args))

src_fh=open(SRC_FILE,'rb');
src_bytes=bytearray(src_fh.read());
src_fh.close();

lbytes=len(src_bytes);
print('source file: '+ SRC_FILE);
print('size: '+ str(lbytes) +'kb');

#for (b in src_bytes):
for i, item in enumerate(src_bytes): 
  if (chr(src_bytes[i])==b'\xff'):
    segmark=SegmentMark.GetSegmentType(chr(src_bytes[i+1]));
    if (segmark!=None):
	    print('Found: '+ segmark['desc'] +' at '+ str(i));

