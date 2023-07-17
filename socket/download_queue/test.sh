#!/usr/bin/env bash

urls=(
  "https://docs.python.org/3/archives/python-3.11.4-docs-pdf-letter.tar.bz2"
  "https://docs.python.org/3/archives/python-3.11.4-docs-pdf-a4.tar.bz2"
)

for url in "${urls[@]}"; do
    resp="$(printf '{"command":"append","url":"%s"}' "$url" | nc -N localhost 8000)"
    if echo "$resp" | jq -e .error >/dev/null; then
        echo "$resp" | jq -r .error
    else
        printf '%d in queue\n' "$(echo "$resp" | jq -r .queue_size)"
    fi
    sleep .1
done
sleep 2
while :; do
    resp="$(printf '{"command":"queue"}' | nc -N localhost 8000)"
    if echo "$resp" | jq -e .error >/dev/null; then
        echo "$resp" | jq -r .error
        exit 1
    else
        queue="$(echo "$resp" | jq .queue_size)"
        case $queue in
            0) echo "done"; exit 0 ;;
            *) echo "$queue left..." ;;
        esac
    fi
    sleep 2
done
