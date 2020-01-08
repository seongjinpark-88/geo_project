#!/bin/bash

# script to begin the docker build process
# NOTE: **MUST** be run from docker/

# OPTIONAL ARGUMENTS
# -w = for windows 10 Home
# -m = set amount of memory docker can use during build (in G)

win=false
mem=8g

while getopts "wm:" opt; do
    case ${opt} in
        w)
            win=true
            ;;
        m)
            mem=${OPTARG}
            ;;
        \?)
            echo "Wrong flags"
            exit 1
            ;;
    esac
done

if [[ ${win} == true ]]; then
    docker build \
        -f docker/WIN/Dockerfile \
        -m ${mem} \
        -t docker-sbt ../
else
    docker build \
        -f docker/UNIX/Dockerfile \
        -m ${mem} \
        -t docker-sbt ../
fi