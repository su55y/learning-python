#!/bin/sh

printRandomDate() {
    date -d "@$(shuf -rz -i 0-9 -n 10)" +%d/%m/%Y
}

printRandomDate
sleep 1
date +%d/%m/%Y
sleep 1
printRandomDate
