#!/bin/bash

# Shell script used to create folder for days 1 to 30 inside docker-lab

mkdir -p docker-lab

for i in $(seq -w 1 30)
do
    mkdir -p docker-lab/day-${i}
    cat <<EOF > docker-lab/day-${i}/README.md
# Day ${i}
:shipit:

## Task

## Solution

## Commands Used

## What I Learned

## Notes
EOF
done