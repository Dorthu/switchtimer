#!/bin/bash
#
# notify-user.sh - a part of switchtimer
#
# This depdnds on notify-send.py to retrieve notifcation IDs and replace
# notifications.
#
# Args:
#  Username is the user we're notifying
#
#  Urgency should be any urgency accepted by notify-send's -u
#  argument.  If not critical, a critical notification will be
#  used to show the notification in full screen applications, then
#  the notification will be replaced by a low-urgency notification
#  to allow it to hide automatically.
USERNAME=$1
URGENCY=$2
shift; shift

# validate inputs
if [[ -z $USERNAME ]]; then
	echo "No username given"
	exit 1
fi

case $URGENCY in
	"critical" | "normal" | "low")
		;;
	*)
		echo 'Urgency must be one of "critical", "medium", or "low"'
		exit 2
		;;
esac

# find the stuff we need for this to work
PATH=/usr/bin:/bin

USER_LINE=$(who | grep $USERNAME)

if [[ $USER_LINE =~ .*\((:[0-9]+)\) ]]; then
	DISPLAY=${BASH_REMATCH[1]}
else
	echo "Not logged in"
	exit 2
fi

DBUS_ADDR=unix:path=/run/user/$(id -u $USERNAME)/bus

# show the notification - if this isn't supposed to be critical, show the notification
# as critical first, then replace it
if [[ $URGENCY != "critical" ]]; then
	MSG_ID=$(sudo -u ${USERNAME} DISPLAY=${DISPLAY} \
		DBUS_SESSION_BUS_ADDRESS=${DBUS_ADDR} \
		PATH=${PATH} \
		notify-send.py \
		-u critical \
		"$@")
	MSG_ID=$(sudo -u ${USERNAME} DISPLAY=${DISPLAY} \
		DBUS_SESSION_BUS_ADDRESS=${DBUS_ADDR} \
		PATH=${PATH} \
		notify-send.py \
		-r $MSG_ID \
		-u $URGENCY \
		"$@")
else
	MSG_ID=$(sudo -u ${USERNAME} DISPLAY=${DISPLAY} \
		DBUS_SESSION_BUS_ADDRESS=${DBUS_ADDR} \
		PATH=${PATH} \
		notify-send.py \
		-u $URGENCY \
		"$@")
fi
