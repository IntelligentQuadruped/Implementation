#1/bin/sh
echo "Running ping.sh"
while true; do
	ping -c 1 google.com
	rc=$?
	if [ $rc -ne 0 ] ; then
		nmcli radio wifi off
		sleep 1
		nmcli radio wifi on
		while true; do
			nmcli c up puwireless
			sleep 1 
			ping -c 1 google.com
			rc=$?
			if [ $rc -eq 0 ] ; then
				break
			fi
		done
	fi	
	sleep 1
done
