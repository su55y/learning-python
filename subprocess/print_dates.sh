#!/bin/sh

printRandomDate() {
    date -d "@$(shuf -i 0-9 -n 10 -z)" +%d/%m/%Y
}

printRandomDate
sleep 1
date +%d/%m/%Y
sleep 1
printRandomDate
