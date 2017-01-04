#!/bin/bash

while [[ $# -gt 1 ]]
do
key="$1"

case $key in
    -f|--file)
    FILE="$2"
    shift # past argument
    ;;
    --default)
    DEFAULT=YES
    ;;
    *)
            # unknown option
    ;;
esac
shift # past argument or value
done

extract_pcap() {
  echo "reading .pcap: ${FILE}";
  END=$(tshark -r ${FILE} -T fields -e tcp.stream | sort -n | tail -1)
  for ((i=0;i<=END;i++))
  do
    echo $i
    tshark -r ${FILE} -o http.decompress_body:TRUE -qz follow,tcp,ascii,$i > follow-stream-$i.txt
  done
}

FILE=${FILE}
[ -a ${FILE} ] && extract_pcap || echo ".pcap file does not exists."

#END=$(tshark -r ../pcap/http.cap -T fields -e tcp.stream | sort -n | tail -1)
#for ((i=0;i<=END;i++))
#do
#  echo $i
#  tshark -r ../pcap/http.cap -qz follow,tcp,ascii,$i > follow-stream-$i.txt
#done
