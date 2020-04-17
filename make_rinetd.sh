#! /bin/bash

echo 'logfile /rinetd_+1s/rinetd.log' > /rinetd_+1s/rinetd.conf

for ((i=$1; i<=$2; i++))
do
	echo '0.0.0.0 ' $i ' 127.0.0.1 64' >> /rinetd_+1s/rinetd.conf
done
