#!/bin/bash
USERNAME=$1
TITLE=$2
MESSAGE=$3
shift

if [[ -z $USERNAME ]]; then
	echo "No username given"
	exit 1
fi

PATH=/usr/bin:/bin

USER_LINE=$(who | grep $USERNAME)

if [[ $USER_LINE =~ .*\((:[0-9]+)\) ]]; then
	DISPLAY=${BASH_REMATCH[1]}
else
	echo "Not logged in"
	exit 2
fi

DBUS_ADDR=unix:path=/run/user/$(id -u $USERNAME)/bus

sudo -u ${USERNAME} DISPLAY=${DISPLAY} \
	DBUS_SESSION_BUS_ADDRESS=${DBUS_ADDR} \
	PATH=${PATH} \
	notify-send "$@"
