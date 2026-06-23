#!/bin/sh
# Button daemon — runs on the Kindle, publishes button events to Edge-NET via
# the kindle-server HTTP bridge. Loops forever; restart on exit via startup.sh.

SERVER="http://192.168.0.61:8080"

# Map lipc keypress scancode → button name
# Kindle 4 scancodes: 193=up 194=down 195=left 196=right 197=select
#                     104=page_back 109=page_fwd 139=menu 158=back 102=home
publish() {
    curl -s -X POST "$SERVER/button/$1" > /dev/null 2>&1 &
}

lipc-wait-event -m -s "" com.lab126.keypad keypress | while read -r line; do
    code=$(echo "$line" | grep -o 'scancode=[0-9]*' | cut -d= -f2)
    case "$code" in
        193) publish "up"       ;;
        194) publish "down"     ;;
        195) publish "left"     ;;
        196) publish "right"    ;;
        197) publish "select"   ;;
        104) publish "page_back";;
        109) publish "page_fwd" ;;
        139) publish "menu"     ;;
        158) publish "back"     ;;
        102) publish "home"     ;;
    esac
done
