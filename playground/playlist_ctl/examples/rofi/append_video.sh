#!/bin/sh

MPV_START_LOCK="/tmp/mpv_start.lock"
MPV_SOCKET_FILE="/tmp/mpv.sock"
RX_URL=".*youtube\.com\/watch\?v=([\w\d_\-]{11})|.*youtu\.be\/([\w\d_\-]{11})"

notify(){ [ -n "$1" ] && notify-send -i mpv -a mpv "$1"; }

[ -f "$MPV_START_LOCK" ] && { notify "MPV process already running..."; exit 1; }

INPUT_URL="$1"
[ -z "$INPUT_URL" ] && INPUT_URL="$(xclip -o -selection clipboard)"
echo "$INPUT_URL" | grep -sqP "$RX_URL" || { notify "invalid url '$INPUT_URL'"; exit 1; }
URL="$(echo "$INPUT_URL" | grep -oP "$RX_URL")"

pidof mpv >/dev/null 2>&1 || {
    touch "$MPV_START_LOCK"
    [ -S "$MPV_SOCKET_FILE" ] && rm "$MPV_SOCKET_FILE"
    setsid -f mpv --idle --no-terminal --input-ipc-server="$MPV_SOCKET_FILE"

    # 5 sec timeout
    for _ in $(seq 50); do
        [ -S "$MPV_SOCKET_FILE" ] && pidof mpv >/dev/null 2>&1 && break
        sleep 0.1
    done

    [ -S "$MPV_SOCKET_FILE" ] || {
        notify "can't find mpv socket file"
        killall mpv
        exit 1
    }
}


append_play(){
    playlist-ctl -a "$1"
    printf '%s' "$(printf '{"command": ["loadfile", "%s", "append-play"]}\n' "$1" |\
        nc -NU "$MPV_SOCKET_FILE" |\
        jq .error)"
}

[ -f "$MPV_START_LOCK" ] && rm "$MPV_START_LOCK"

case $(append_play "$URL") in
*success*) notify "video added to playlist: $URL" ;;
*) notify "can't add video: $URL" ;;
esac
