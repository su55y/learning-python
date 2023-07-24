#!/bin/sh

MPV_SOCKET_FILE="/tmp/mpv.sock"

[ -S "$MPV_SOCKET_FILE" ] || { printf '\000message\037%s not found\n' "$MPV_SOCKET_FILE"; exit 1; }

play_index(){
    printf '%s' "$(printf '{"command": ["playlist-play-index", "%s"]}\n' "$1" |\
        nc -NU "$MPV_SOCKET_FILE" |\
        jq .error)"
}

case $ROFI_RETV in
0) playlist-ctl ;;
1)
    error="$(play_index "$ROFI_INFO")"
    case $error in
    *success*) exit 0 ;;
    *)
        printf '\000message\037%s\n' "$error"
        pidof mpv >/dev/null 2>&1 || echo "mpv process not found"
    ;;
    esac
;;
esac
