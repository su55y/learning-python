#!/usr/bin/env bash

urls=(
  "https://docs.python.org/3/archives/python-3.11.4-docs-pdf-letter.tar.bz2"
  "https://docs.python.org/3/archives/python-3.11.4-docs-pdf-a4.tar.bz2"
  "https://docs.python.org/3/archives/python-3.11.4-docs-html.tar.bz2"
)

for url in "${urls[@]}"; do
    queue="$(echo "$url" | nc -N localhost 8000 || exit 1)"
    echo "$queue in queue"
done
sleep 1
while :; do
    queue="$(echo "queue" | nc -N localhost 8000)"
    case $queue in
        0) echo "done"; echo "stop" | nc -N localhost 8000; exit 0 ;;
        *) echo "$queue left..." ;;
    esac
    sleep 1
done
