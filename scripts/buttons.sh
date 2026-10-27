#!/bin/sh
# Button daemon — runs on the Kindle, reads raw key events from the K4's input
# devices and publishes them to Edge-NET via the kindle-server HTTP bridge.
# Needs the Kindle framework stopped (startup.sh does it): the framework grabs
# these devices exclusively and nothing else ever sees a press.

SERVER="http://192.168.0.57"   # nginx-proxy, see poll.sh

publish() {
    curl -s -X POST "$SERVER/button/$1" > /dev/null 2>&1 &
}

# evdev key codes captured from this K4 on 2026-10-27.
name_for() {
    case "$1" in
        103) echo up ;;
        108) echo down ;;
        105) echo left ;;
        106) echo right ;;
        194) echo select ;;
        # shortcut: which side 191/193 sit on was guessed; swap them if one side's page keys are reversed.
        104|191) echo page_back ;;
        109|193) echo page_fwd ;;
    esac
}

# One reader per device. fd 3 stays open between reads so no event is lost.
# Each read is one 16-byte input_event: sec(2) usec(2) type code value(2) as u16s.
read_device() {
    exec 3< "$1"
    while :; do
        set -- $(dd bs=16 count=1 <&3 2>/dev/null | hexdump -v -e '8/2 "%u " "\n"')
        [ -n "$5" ] || { sleep 1; continue; }   # device error: don't spin
        [ "$5" = 1 ] && [ "$7" = 1 ] || continue   # type 1 = key, value 1 = press
        n=$(name_for "$6")
        [ -n "$n" ] && publish "$n"
    done
}

read_device /dev/input/event0 &   # tequila-keypad: page-turn keys
read_device /dev/input/event1     # fiveway: d-pad + select
