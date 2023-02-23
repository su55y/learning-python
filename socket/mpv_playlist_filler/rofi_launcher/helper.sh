#!/bin/sh

# activate hotkeys
#printf "\000use-hot-keys\037true\n"

play_index(){
  printf '%s' "$(printf '{"command": ["playlist-play-index", "%s"]}\n' "$1" |\
    nc -NU /tmp/mpv.sock |\
    jq .error)"
}

print_playlist(){
  while read -r entry || [ "$entry" ]; do
    id="${entry%% *}"
    title="${entry#* }"
    printf '%s\000info\037%s\n' "$title" "$id"
  done < /tmp/mpv_current_playlist
}

case $ROFI_RETV in
    0) print_playlist ;;
    1)
      case $(play_index "$ROFI_INFO") in
        *success*) exit 0 ;;
        *) echo "some error occurred, check logs" ;;
      esac
    ;;
esac
